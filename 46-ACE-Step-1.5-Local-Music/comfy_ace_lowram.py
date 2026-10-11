"""Process-local ACE text-encoder loader; ComfyUI files and model weights stay unchanged.

Construct ACE encoder parameters on meta, then assign existing safetensors tensors.
This avoids a second full initialized parameter allocation during loading. Native
ComfyUI model patching, graph nodes, generation parameters and weights are retained.
"""
from pathlib import Path
import argparse,inspect,os,runpy,sys

def main():
    p=argparse.ArgumentParser();p.add_argument('--comfyui',type=Path,required=True);a,rest=p.parse_known_args();base=a.comfyui.resolve();assert(base/'main.py').is_file()
    os.chdir(base);sys.path.insert(0,str(base));sys.argv=[str(base/'main.py')]+rest
    # ComfyUI parses its arguments during these imports; keep normal server options.
    import comfy.options
    comfy.options.enable_args_parsing()
    import torch,comfy.sd,comfy.sd1_clip
    def release_consumed_cpu_pages():
        # Windows can keep consumed mmap pages in this process's working set.
        # Release only this server's resident CPU pages after a synchronous GPU copy.
        if os.name=='nt':
            import ctypes
            from ctypes import wintypes
            kernel=ctypes.windll.kernel32;api=ctypes.windll.psapi
            kernel.GetCurrentProcess.restype=wintypes.HANDLE
            api.EmptyWorkingSet.argtypes=[wintypes.HANDLE];api.EmptyWorkingSet.restype=wintypes.BOOL
            if not api.EmptyWorkingSet(kernel.GetCurrentProcess()):raise OSError('Own working-set release failed')
    original_clip_init=comfy.sd.CLIP.__init__;original_load_sd=comfy.sd.CLIP.load_sd
    def load_sd(self,sd,full_model=False):
        is_ace='ACE15TEModel'in type(self.cond_stage_model).__name__
        if is_ace and any(p.is_meta for p in self.cond_stage_model.parameters()):
            if full_model:return self.cond_stage_model.load_state_dict(sd,strict=False,assign=True)
            # Stream one checkpoint tensor to its native target dtype/device at a time.
            # Do not retain a complete CPU encoder while making a complete GPU copy.
            small=sd['model.layers.0.post_attention_layernorm.weight'].shape[0]==1024
            component=self.cond_stage_model.qwen3_06b if small else getattr(self.cond_stage_model,self.cond_stage_model.lm_model)
            targets=component.transformer.state_dict()
            for key in list(sd):
                if key in targets and isinstance(sd[key],torch.Tensor):
                    sd[key]=sd[key].to(device=self.patcher.load_device,dtype=targets[key].dtype)
                    if sd[key].numel()*sd[key].element_size()>=16*1024**2:release_consumed_cpu_pages()
            for module in self.cond_stage_model.modules():module.can_assign_sd=True
            return self.cond_stage_model.load_sd(sd)
        return original_load_sd(self,sd,full_model)
    def clip_init(self,*args,**kwargs):
        bound=inspect.signature(original_clip_init).bind(self,*args,**kwargs);target=bound.arguments.get('target')
        if target is not None and getattr(target,'clip',None)is not None and 'ACE15TEModel'in target.clip.__name__:
            options=dict(bound.arguments.get('model_options')or {});options['initial_device']=torch.device('meta');bound.arguments['model_options']=options
            original_clip_init(*bound.args,**bound.kwargs)
            missing=[name for name,parameter in self.cond_stage_model.named_parameters()if parameter.is_meta]
            if missing:raise RuntimeError('Incomplete ACE meta assignment: '+', '.join(missing[:8]))
            print('ACE low-RAM loader: existing weights assigned; no meta parameters remain',flush=True)
        else:original_clip_init(self,*args,**kwargs)
    comfy.sd.CLIP.load_sd=load_sd;comfy.sd.CLIP.__init__=clip_init
    runpy.run_path(str(base/'main.py'),run_name='__main__')
if __name__=='__main__':main()
