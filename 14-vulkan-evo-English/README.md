# llama.cpp on AMD: Vulkan Setup & Checks | Strix Halo

Companion package for the English episode.

1. Verify an AMD graphics driver with Vulkan support.
2. INSTALL-LLAMA.ps1 downloads the complete official b11078 archive into a NEW folder and verifies SHA256.
3. Inspect --version and --list-devices to confirm GPU detection.
4. Download a compatible GGUF separately; check its license, architecture and free memory.
5. START-LLAMA.ps1 -Installation "C:\your\Dolmario-Vulkan" -ModelPath "D:\Models\your-model.gguf".
6. Keep the server terminal open. Run TEST-API.ps1 in another terminal; browser http://127.0.0.1:8091.
7. Stop only your own server with Ctrl+C.

## Teststand / Evidence

Evidence: GPU detection checked on 22 September 2026 with existing build 10621 (c1d0e7a00). b11078 is a download example verified against official release metadata; no clean installation or new model run today. Models such as Flash Next may require a different build. 999 GPU layers do not create memory. These workflows are launch/API-test templates, not ComfyUI graphs.

Read the PowerShell files first. From the extracted companion folder run .\Filename.ps1. Do not globally disable ExecutionPolicy. If Windows blocks a downloaded file, inspect it before locally unblocking that specific file. INSTALL creates a new directory; START loads a model and needs free resources. No administrator rights assumed.

## Quellen / Sources

Pinned official release (example, not the latest release):
https://github.com/ggml-org/llama.cpp/releases/tag/b11078
Pinned server documentation:
https://github.com/ggml-org/llama.cpp/blob/b11078/tools/server/README.md
Installation overview:
https://github.com/ggml-org/llama.cpp/blob/master/docs/install.md
Archive SHA256 from official GitHub release API, checked 2026-10-05:
0649f258e140a8b3b1a4c58d863c317b0fd3427eed2e72132399dbde363df861
