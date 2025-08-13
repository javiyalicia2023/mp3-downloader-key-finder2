
# Descargador de MP3 y analizador de tonalidad

Esta herramienta descarga el audio de un enlace de YouTube, lo convierte a MP3 
(160 kbps o 320 kbps) y analiza la pista para obtener:

- Tonalidad principal y tonalidad relativa
- BPM (tempo)
- Niveles de energía, bailabilidad y felicidad (0‑100)

Todo el proyecto puede utilizarse desde la línea de comandos o mediante una 
pequeña interfaz gráfica.

## Instalación rápida en Windows

1. Descarga o clona este repositorio.
2. Abre PowerShell **como administrador** dentro de la carpeta del proyecto.
3. Ejecuta:
   ```powershell
   ./setup.ps1
   ```
   El script instalará Python, FFmpeg y todas las dependencias, y generará los
   ejecutables en `dist/`.

## Uso por línea de comandos

```bash
python main.py <URL_YOUTUBE> [--bitrate 160|320] [--lang es|en]
```

El archivo MP3 se guarda en la carpeta `downloads/` y en pantalla se muestran la
clave detectada, la tonalidad relativa y las métricas de BPM, energía,
bailabilidad y felicidad. Usa `--lang` para elegir idioma (español o inglés).

## Interfaz gráfica

```bash
python gui.py [es|en]
```

La GUI utiliza una paleta negro/#2F5BF9/blanco. Permite seleccionar la carpeta
de descarga, introducir un enlace de YouTube o arrastrar archivos de audio para
analizarlos.

## Métricas de audio

Las puntuaciones de energía, bailabilidad y felicidad se expresan en una escala
0‑100. Se interpretan así:

- 0–33 → nivel **bajo**
- 34–66 → nivel **medio**
- 67–100 → nivel **alto**

## Construir ejecutables manualmente

Si ya tienes Python y FFmpeg instalados, instala las dependencias con:

```bash
pip install -r requirements.txt
```

Luego ejecuta:

```bash
python build.py cli  # ejecutable de línea de comandos
python build.py gui  # ejecutable con interfaz gráfica
```

Los binarios resultantes se guardan en `dist/`.