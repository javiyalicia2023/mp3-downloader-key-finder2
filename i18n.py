LANG = 'en'

TRANSLATIONS = {
    'en': {
        'app_title': 'MP3 Downloader & Analyzer',
        'download_directory': 'Download directory:',
        'browse': 'Browse',
        'youtube_url': 'YouTube URL:',
        'download': 'Download',
        'files': 'Files:',
        'file': 'File',
        'analyze_selected': 'Analyze Selected',
        'import_analyze': 'Import and Analyze File',
        'drop_audio': 'Drop audio file here',
        'error': 'Error',
        'enter_url': 'Please enter a YouTube URL.',
        'download_error': 'Download error',
        'info': 'Info',
        'select_file': 'Select a file to analyze.',
        'cli_description': 'Download YouTube audio and estimate its key',
        'arg_url': 'YouTube video URL',
        'arg_output_dir': 'Directory where the MP3 will be saved',
        'arg_lang': 'Interface language (en or es)',
        'audio_saved': 'Audio saved to {}',
        'detected_key': 'Detected key',
        'relative_key': 'Relative key',
        'bpm': 'BPM',
        'energy': 'Energy',
        'danceability': 'Danceability',
        'happiness': 'Happiness',
        'low': 'low',
        'medium': 'medium',
        'high': 'high',
    },
    'es': {
        'app_title': 'Descargador MP3 y Analizador',
        'download_directory': 'Carpeta de descarga:',
        'browse': 'Buscar',
        'youtube_url': 'URL de YouTube:',
        'download': 'Descargar',
        'files': 'Archivos:',
        'file': 'Archivo',
        'analyze_selected': 'Analizar seleccionado',
        'import_analyze': 'Importar y analizar archivo',
        'drop_audio': 'Suelta el archivo de audio aquí',
        'error': 'Error',
        'enter_url': 'Por favor introduce una URL de YouTube.',
        'download_error': 'Error de descarga',
        'info': 'Información',
        'select_file': 'Selecciona un archivo para analizar.',
        'cli_description': 'Descarga audio de YouTube y estima su tonalidad',
        'arg_url': 'URL de video de YouTube',
        'arg_output_dir': 'Directorio donde se guardará el MP3',
        'arg_lang': 'Idioma de la interfaz (en o es)',
        'audio_saved': 'Audio guardado en {}',
        'detected_key': 'Tonalidad detectada',
        'relative_key': 'Tonalidad relativa',
        'bpm': 'BPM',
        'energy': 'Energía',
        'danceability': 'Bailabilidad',
        'happiness': 'Felicidad',
        'low': 'baja',
        'medium': 'media',
        'high': 'alta',
    }
}


def set_language(lang: str) -> None:
    global LANG
    if lang in TRANSLATIONS:
        LANG = lang


def t(key: str) -> str:
    return TRANSLATIONS.get(LANG, TRANSLATIONS['en']).get(key, key)
