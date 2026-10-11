"""One bounded ACE-Step 1.5 ComfyUI job; never stops or reconfigures a server."""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlencode,urlsplit
import argparse,hashlib,ipaddress,json,time,uuid

MODELS={'unet':'acestep_v1.5_turbo.safetensors','clip1':'qwen_0.6b_ace15.safetensors','clip2':'qwen_4b_ace15.safetensors','vae':'ace_1.5_vae.safetensors'}
def graph(v,seed,prefix):
    return {
      '1':dict(class_type='UNETLoader',inputs=dict(unet_name=MODELS['unet'],weight_dtype='default')),
      '2':dict(class_type='ModelSamplingAuraFlow',inputs=dict(model=['1',0],shift=3)),
      '3':dict(class_type='DualCLIPLoader',inputs=dict(clip_name1=MODELS['clip1'],clip_name2=MODELS['clip2'],type='ace',device='default')),
      '4':dict(class_type='VAELoader',inputs=dict(vae_name=MODELS['vae'])),
      '5':dict(class_type='TextEncodeAceStepAudio1.5',inputs=dict(clip=['3',0],tags=v['tags'],lyrics=v['lyrics'],seed=seed,bpm=v['bpm'],duration=float(v['seconds']),timesignature='4',language='en',keyscale=v['key'],generate_audio_codes=True,cfg_scale=2.0,temperature=.85,top_p=.9,top_k=0,min_p=0.)),
      '6':dict(class_type='ConditioningZeroOut',inputs=dict(conditioning=['5',0])),
      '7':dict(class_type='EmptyAceStep1.5LatentAudio',inputs=dict(seconds=float(v['seconds']),batch_size=1)),
      '8':dict(class_type='KSampler',inputs=dict(model=['2',0],seed=seed,steps=8,cfg=1.,sampler_name='euler',scheduler='simple',positive=['5',0],negative=['6',0],latent_image=['7',0],denoise=1.)),
      '9':dict(class_type='VAEDecodeAudio',inputs=dict(samples=['8',0],vae=['4',0])),
      '10':dict(class_type='SaveAudio',inputs=dict(audio=['9',0],filename_prefix=prefix))}

def server_address(value):
    p=urlsplit(value)
    try:local=p.hostname=='localhost' or ipaddress.ip_address(p.hostname or '').is_loopback
    except ValueError:local=False
    if p.scheme!='http' or not local or p.username or p.password or p.query or p.fragment or p.path not in ('','/'):
        raise ValueError('Use a plain HTTP loopback ComfyUI server address')
    return value.rstrip('/')

def request(server,path,data=None):
    req=Request(server+path,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json'})
    with urlopen(req,timeout=60)as r:return json.load(r)

def main():
    p=argparse.ArgumentParser();p.add_argument('--server',default='http://127.0.0.1:8189');p.add_argument('--variant',type=Path,default=Path(__file__).with_name('variant.json'));p.add_argument('--output',type=Path,default=Path('new-song'));p.add_argument('--timeout',type=float,default=1800);a=p.parse_args()
    server=server_address(a.server);v=json.loads(a.variant.read_text('utf-8'))
    if not 1<=float(v['seconds'])<=60:raise ValueError('This AMD example permits only 1..60 seconds; do not raise the limit')
    if a.output.exists():raise FileExistsError('Choose a new output directory')
    queue=request(server,'/queue')
    if queue['queue_running'] or queue['queue_pending']:raise RuntimeError('Server busy; wait for current work')
    stats=request(server,'/system_stats')
    if stats['system']['ram_free']<6*2**30:raise RuntimeError('Less than6GiB free physical RAM; do not start this job')
    workflow=graph(v,int(v['seed']),'audio/dolmario_tutorial_'+str(uuid.uuid4()))
    started=time.perf_counter();answer=request(server,'/prompt',dict(prompt=workflow,client_id=str(uuid.uuid4())))
    if answer.get('node_errors'):raise RuntimeError(str(answer['node_errors']))
    prompt_id=answer['prompt_id'];a.output.mkdir();(a.output/'workflow-api.json').write_text(json.dumps(workflow,indent=2)+'\n','utf-8')
    while time.perf_counter()-started<a.timeout:
        stats=request(server,'/system_stats')
        if stats['system']['ram_free']<6*2**30:
            request(server,'/interrupt',dict(prompt_id=prompt_id))
            raise RuntimeError('RAM guard: requested interruption of this prompt ID only; own output retained')
        result=request(server,'/history/'+prompt_id)
        if prompt_id in result:
            entry=result[prompt_id];status=entry.get('status',{})
            if status.get('status_str')!='success':raise RuntimeError('Own job failed: '+str(status))
            files=[r for node in entry['outputs'].values() for group in node.values() if isinstance(group,list) for r in group if isinstance(r,dict) and str(r.get('filename','')).endswith(('.flac','.wav','.mp3','.opus'))]
            if not files:raise RuntimeError('No audio file in completed job')
            spec=files[0]
            with urlopen(server+'/view?'+urlencode({k:spec[k]for k in ('filename','subfolder','type')}),timeout=120)as response:audio=response.read()
            dest=a.output/('song'+Path(spec['filename']).suffix);dest.write_bytes(audio)
            report=dict(seconds=time.perf_counter()-started,variant=v,prompt_id=prompt_id,audio_sha256=hashlib.sha256(audio).hexdigest(),output_name=dest.name,history=entry)
            (a.output/'REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
            print('Completed',dest.name,round(report['seconds'],2),'seconds',flush=True);return
        print('Own job running',round(time.perf_counter()-started),'seconds',flush=True);time.sleep(2)
    raise TimeoutError('Own job timeout; inspect its prompt ID and server. No foreign process was stopped.')
if __name__=='__main__':main()
