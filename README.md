# speech_to_text: Speech-to-Text con Vosk y SoundDevice

Este script de Python permite la transcripción de voz a texto utilizando la biblioteca Vosk para el reconocimiento de voz y SoundDevice para la manipulación de audio. Puede transcribir audio en tiempo real desde un micrófono o procesar un archivo de audio WAV preexistente. También ofrece la opción de guardar la grabación de audio (desde el micrófono) y la transcripción resultante.

Este proyecto se encuentra en el repositorio [speech_to_text](https://github.com/slrosales/speech_to_text) en GitHub, perfil de `slrosales`.

## Características

*   Transcripción en tiempo real desde el micrófono.
*   Transcripción desde archivos de audio WAV.
*   Posibilidad de guardar el audio capturado desde el micrófono en formato RAW.
*   Posibilidad de guardar la transcripción en un archivo de texto (`.txt`).
*   Listado de dispositivos de audio disponibles.
*   Selección de dispositivo de entrada, tasa de muestreo y modelo de lenguaje Vosk.

## Requisitos

Antes de ejecutar el script, asegúrate de tener instaladas las siguientes dependencias:

```sh
pip install sounddevice vosk numpy
```
(Aunque `wave` y `json` son usados, son parte de la biblioteca estándar de Python y no requieren instalación separada).

## Descarga del Modelo Vosk

Necesitarás descargar un modelo de lenguaje de Vosk para el idioma que desees transcribir. Puedes encontrar una lista de modelos disponibles en el [sitio web de Vosk](https://alphacephei.com/vosk/models).

Por ejemplo, para descargar el modelo en español (uno de los modelos disponibles, verifica el sitio para el más adecuado a tus necesidades o el que coincida con el usado por defecto en el script si no usas `-m`):

```sh
wget https://alphacephei.com/vosk/models/vosk-model-es-0.42.zip
unzip vosk-model-es-0.42.zip
# Esto creará una carpeta, por ejemplo, 'vosk-model-es-0.42'
```

**Importante:** Anota la ruta donde descomprimes el modelo, ya que la necesitarás para el argumento `-m` o deberás asegurarte de que la ruta por defecto en el script (`vosk-model-es-0.42`) sea accesible. **Se recomienda encarecidamente usar el argumento `-m` para especificar la ruta a tu modelo descargado.**

## Uso

Ejecuta el script desde la línea de comandos:

```sh
python tu_script.py [OPCIONES]
```
(Reemplaza `tu_script.py` con el nombre real de tu archivo Python).

### Opciones

| Opción                               | Descripción                                                                                                                                                                 |
| :----------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-l, --list-devices`                 | Muestra la lista de dispositivos de audio disponibles y sale.                                                                                                               |
| `-f, --filename FILENAME`            | Especifica un archivo (formato RAW) donde se guardará la grabación de audio capturada desde el micrófono.                                                                 |
| `-t, --transcription-file TRANSCRIPTION_FILE` | Especifica un archivo (formato TXT) donde se guardará la transcripción resultante.                                                                                  |
| `-i, --input-file INPUT_FILE`        | Especifica un archivo de audio WAV para transcribir (en lugar de usar el micrófono). Si se usa, la opción `-f` se ignora.                                                  |
| `-d, --device DEVICE`                | Selecciona el dispositivo de entrada de audio (ID numérico o una subcadena del nombre del dispositivo).                                                                     |
| `-r, --samplerate SAMPLERATE`        | Define la tasa de muestreo del audio. Si no se especifica, se intentará autodetectar desde el dispositivo de entrada o desde el archivo WAV de entrada.                      |
| `-m, --model MODEL_PATH`             | Especifica la ruta a la carpeta del modelo de lenguaje Vosk que se utilizará. Si no se proporciona, el script intentará usar `"vosk-model-es-0.42"` en la misma carpeta. |

### Ejemplos de uso

1.  **Listar los dispositivos de audio disponibles:**
    ```sh
    python tu_script.py --list-devices
    ```

2.  **Transcribir desde el micrófono usando un dispositivo específico, guardar la grabación y la transcripción, especificando el modelo:**
    ```sh
    python tu_script.py -d 1 -f audio_grabado.raw -t transcripcion.txt -m ruta/a/tu/vosk-model-es-0.42
    ```
    (Reemplaza `1` con el ID de tu micrófono y `ruta/a/tu/vosk-model-es-0.42` con la ruta real a tu modelo).

3.  **Transcribir desde el micrófono, solo guardar la transcripción, usando el modelo por defecto (si está en la ruta esperada o especificado con `-m`):**
    ```sh
    python tu_script.py -t transcripcion_microfono.txt -m ruta/a/tu/modelo_vosk
    ```

4.  **Transcribir un archivo de audio WAV y guardar la transcripción:**
    ```sh
    python tu_script.py -i mi_audio.wav -t transcripcion_archivo.txt -m ruta/a/tu/vosk-model-en-us
    ```
    (Asegúrate de que el modelo (`-m`) corresponda al idioma del audio en `mi_audio.wav`).

5.  **Transcribir desde el micrófono usando el modelo por defecto (asumiendo que `vosk-model-es-0.42` existe en la ubicación correcta) y solo mostrar en consola (sin guardar en archivo):**
    ```sh
    python tu_script.py
    ```
    *Nota: La transcripción en tiempo real desde el micrófono se imprimirá en la consola si no se especifica `-t`. Si se especifica `-t`, se guardará en el archivo.*

## Notas

*   Para detener la grabación/transcripción desde el micrófono, presiona `Ctrl + C`.
*   El script utiliza `vosk-model-es-0.42` como la ruta del modelo por defecto si no se especifica el argumento `-m`. Asegúrate de que esta carpeta del modelo exista en el mismo directorio que el script, o **(recomendado)** usa siempre el argumento `-m` para proporcionar la ruta explícita al modelo que has descargado.
*   Puedes usar cualquier modelo de Vosk compatible. Simplemente descarga el modelo, descomprímelo y proporciona la ruta a la carpeta del modelo mediante el argumento `-m`.
*   Si transcribes un archivo (`-i`), el script procesará el archivo completo y luego guardará la transcripción si se especifica `-t`.
*   Si transcribes desde el micrófono y se especifica `-t`, la transcripción se irá guardando en el archivo a medida que se reconoce.