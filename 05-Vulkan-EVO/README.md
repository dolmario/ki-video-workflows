# llama.cpp auf AMD: Vulkan einrichten und prüfen | Strix Halo

Begleitpaket fuer die deutsche Folge.

1. AMD-Grafiktreiber mit Vulkan-Unterstuetzung pruefen.
2. INSTALL-LLAMA.ps1 laedt das komplette offizielle b11078-Archiv in einen NEUEN Ordner und prueft SHA256.
3. --version und --list-devices ansehen; richtige GPU nachweisen.
4. Passendes GGUF separat laden; Lizenz, Modellarchitektur und freien Speicher pruefen.
5. START-LLAMA.ps1 -Installation "C:\dein\Dolmario-Vulkan" -ModelPath "D:\Modelle\dein-modell.gguf".
6. Serverterminal offen lassen. In zweitem Terminal TEST-API.ps1; Browser http://127.0.0.1:8091.
7. Nur den selbst gestarteten Server mit Strg+C beenden.

## Teststand / Evidence

Belegt: GPU-Erkennung am 22.09.2026 mit vorhandenem Build 10621 (c1d0e7a00). b11078 ist ein anhand offizieller Release-Metadaten geprueftes Downloadbeispiel; heute nicht frisch installiert und kein neuer Modelllauf. Spezielle Modelle wie Flash Next koennen einen anderen Build brauchen. 999 GPU-Schichten schaffen keinen zusaetzlichen Speicher. Diese Workflow-Dateien sind Start- und API-Testvorlagen, keine ComfyUI-Graphen.

Die PowerShell-Dateien vorher lesen. In PowerShell im entpackten Begleitordner mit .\Dateiname.ps1 starten. Keine ExecutionPolicy global abschalten. Falls Windows blockiert: nach Dateipruefung nur die betreffenden selbst heruntergeladenen Skripte lokal entsperren. INSTALL erstellt einen neuen Ordner; START laedt ein Modell und benoetigt freie Ressourcen. Keine Administratorrechte vorausgesetzt.

## Quellen / Sources

Pinned official release (example, not the latest release):
https://github.com/ggml-org/llama.cpp/releases/tag/b11078
Pinned server documentation:
https://github.com/ggml-org/llama.cpp/blob/b11078/tools/server/README.md
Installation overview:
https://github.com/ggml-org/llama.cpp/blob/master/docs/install.md
Archive SHA256 from official GitHub release API, checked 2026-10-05:
0649f258e140a8b3b1a4c58d863c317b0fd3427eed2e72132399dbde363df861
