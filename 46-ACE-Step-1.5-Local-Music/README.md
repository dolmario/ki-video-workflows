# ACE-Step 1.5 local song: short ComfyUI companion

Actual60-second AMD test workflow, original English example lyrics, API helper and editable node graph. No band music, Sickheadz lyrics, model weights, or voice recordings are bundled.

## Models and ComfyUI

Use a working [ComfyUI](https://github.com/Comfy-Org/ComfyUI) installation including `TextEncodeAceStepAudio1.5`, `EmptyAceStep1.5LatentAudio`, `VAEDecodeAudio` and `SaveAudio`. Download these four files from [Comfy-Org's official distribution](https://huggingface.co/Comfy-Org/ace_step_1.5_ComfyUI_files/tree/main):

| Folder below ComfyUI/models | File |
|---|---|
| diffusion_models | acestep_v1.5_turbo.safetensors |
| text_encoders | qwen_0.6b_ace15.safetensors |
| text_encoders | qwen_4b_ace15.safetensors |
| vae | ace_1.5_vae.safetensors |

Combined approximately14.7GB. [Upstream code license](https://github.com/ace-step/ACE-Step-1.5/blob/main/LICENSE) is MIT; the linked Comfy-Org model card declares Apache2.0. Consult the actual licenses for the files you use. These terms do not override rights in supplied lyrics/images. The Opera images used FLUX.2dev non-commercial terms.

Start your own ComfyUI installation on loopback, with its working GPU environment:

```powershell
python comfy_ace_lowram.py --comfyui C:\ComfyUI --listen 127.0.0.1 --port 8189 --gpu-only --disable-pinned-memory --disable-async-offload --offline --disable-all-custom-nodes
```

Do not start a second server on an occupied port. Wait for other work to finish and ensure free physical/device memory. The tutorial uses an existing working environment; clean installation on another machine is not claimed as validated.

## Reproduce the short example

Load `workflow-ui.json` into ComfyUI for an editable graph, or run the standard-library API helper from this folder:

```powershell
python musik_erzeugen.py --variant variant.json --output new-song
```

The server must already be running and its queue empty. `--server` changes its loopback address. The helper preserves existing output and never stops a server. A new directory stores the exact API graph, returned history, measurement and original audio.

Tags describe genre/instruments/vocal style. `bpm=150`, Dminor,4/4, `language=en`,60seconds, seed11. Lyrics use verse/chorus markers. Text encoder cfg2/temperature0.85/top_p0.9; sampler8steps, Euler/simple, cfg1; model shift3. Edit one parameter at a time and listen to every whole candidate. Lyrics need not be perfectly intelligible in every generation.

This AMD example refuses durations over60seconds. A previous190-second EVO-X2 job crashed the host. Monitor free RAM during the run and stop only your own process if it falls below6GiB. For multiple seeds, restart your own ComfyUI process between jobs. Joining short sections needs tempo/key/transition editing; it is not a verified substitute for a coherent single six-minute song.

## Gaps and levels

```powershell
ffmpeg -i candidate.flac -af silencedetect=noise=-45dB:d=0.4 -f null -
ffmpeg -i candidate.flac -af loudnorm=I=-18:TP=-2:LRA=9 -ar 48000 edit-copy.wav
```

Listen around each gap: rests and fades can be intentional. Preserve original files; loudness-match separate comparison copies. Use measured two-pass normalization for final delivery.

The full364-second Midnight Opera metal song is separate returned RTX3090Ti material: roughly275–300s generation, with earlier60s tests around15s. Those are measured historical runs, not AMD timing promises. The tutorial's newly recorded AMD result is documented separately. No lip-sync validation is claimed for the Opera images.


## AMD loading route and full-song workflow

Run the command above with the Python of your working ComfyUI GPU environment; replace C:\ComfyUI with its actual folder. The process-local wrapper constructs ACE encoder parameters on meta and transfers/assigns checkpoint tensors one by one in the native target dtype. On Windows it releases consumed CPU mmap working-set pages of this server only. ComfyUI files and weights remain unchanged, no unsupported DynamicVRAM mode is forced, and the 6 GiB physical RAM guard is retained by the production monitor. Keep memory monitoring on your own run.

For the returned full RTX 3090 Ti song, load workflow-rtx3090ti-song-ui.json into your own fresh ComfyUI instance. Both duration fields are 364 s; seed 11, original Opera lyrics, 150 BPM/D minor. The matching API graph and variant are included. Use this full-song workflow only on hardware with separately established headroom; the bounded AMD helper intentionally refuses it. Native full-song generation was measured on the returned 3090 Ti route, not as a new AMD full-song test.
