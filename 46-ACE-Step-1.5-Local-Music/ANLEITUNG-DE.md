# Eigenen kurzen Song mit ACE-Step1.5 erzeugen

Vier Modelle aus der offiziellen Comfy-Org-Verteilung in die passenden ComfyUI-Ordner legen: Turbo in `diffusion_models`, qwen0.6b/qwen4b in `text_encoders`, ace1.5VAE in `vae`. Zusammen etwa14,7GB. Aktuelle ComfyUI-Knoten nötig; Details und Primärquellen in README.md. Quellcode MIT, Comfy-Org-Modellkarte Apache2.0; tatsächliche Dateilizenzen prüfen.

Eine eigene freie ComfyUI-Instanz mit deren GPU-Python starten:

```powershell
python comfy_ace_lowram.py --comfyui C:\ComfyUI --listen 127.0.0.1 --port 8189 --gpu-only --disable-pinned-memory --disable-async-offload --offline --disable-all-custom-nodes
```

Im Begleitordner `workflow-ui.json` laden oder mit Standard-Python:

```powershell
python musik_erzeugen.py --variant variant.json --output neuer-song
```

Queue muss leer sein. Ein neuer Ausgabeordner erhält tatsächlichen API-Graph, Ergebnis, Zeitmessung und Originalton. Der Helfer beendet keine Prozesse. Tags,150BPM,d-Moll,4/4,Englisch,eigene Lyrics und60Sekunden einstellen. Seed11,8Euler-Schritte/simple/cfg1; Modellshift3. Nur einen Wert je Versuch ändern und den gesamten Kandidaten anhören.

Der AMD-Beispielhelfer verweigert mehr als60Sekunden. Ein190-Sekunden-Versuch brachte den EVO-X2 zum Absturz. Freien RAM beobachten, bei weniger als6GiB nur eigene Produktion stoppen. Eigene ComfyUI zwischen Seeds neu starten. Abschnitte benötigen musikalisch geprüfte Übergänge; Aneinanderhängen ist kein Nachweis eines stimmigen langen Songs.

```powershell
ffmpeg -i kandidat.flac -af silencedetect=noise=-45dB:d=0.4 -f null -
```

Stille Stellen anhören, Original sichern, Pegel in einer Schnittkopie angleichen. Die364-Sekunden-Oper stammt separat von der RTX3090Ti (etwa275–300s Erzeugung); dortige60-Sekunden-Messung rund15s ist kein AMD-Zeitversprechen. Keine Bandaufnahmen oder Sickheadz-Lyrics im Download; Beispieltext ist eigenständig.


## AMD-Ladeweg und vollständiger Song

Den obigen Startbefehl mit dem GPU-Python der vorhandenen ComfyUI-Umgebung ausführen; C:\ComfyUI durch deren tatsächlichen Ordner ersetzen. Der separate Prozessloader baut ACE-Encoder zunächst auf meta und überträgt/ordnet Checkpoint-Tensoren einzeln im nativen Zieldatentyp zu. Unter Windows werden verbrauchte CPU-mmap-Arbeitssatzseiten nur dieser eigenen Instanz freigegeben. ComfyUI-Dateien und Gewichte bleiben unverändert. Kein erzwungenes inkompatibles DynamicVRAM und keine abgesenkte 6-GiB-RAM-Schutzgrenze. Speicher beim eigenen Lauf weiter überwachen.

Für den vollständigen zurückgegebenen RTX-3090-Ti-Song workflow-rtx3090ti-song-ui.json in einer eigenen frisch gestarteten ComfyUI laden: beide Längenfelder 364 s, Seed 11, eigene Opernlyrics, 150 BPM/d-Moll. API-Graph und Variantenwerte enthalten. Nur mit dafür nachgewiesenem Hardware-Spielraum verwenden; der begrenzte AMD-Helfer verweigert diese Länge bewusst. Ein neuer vollständiger AMD-Songlauf wird nicht behauptet.
