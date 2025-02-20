# Speech-to-Text with Vosk and SoundDevice

Este script permite la transcripción de voz a texto en tiempo real usando la biblioteca Vosk y SoundDevice en Python.

## Requisitos

Antes de ejecutar el script, asegúrate de tener instaladas las siguientes dependencias:

```sh
pip install sounddevice vosk numpy
```

Además, descarga el modelo de Vosk correspondiente al idioma que deseas utilizar, por ejemplo, el modelo en español:

```sh
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip
```

## Uso

Ejecuta el script con las siguientes opciones:

```sh
python script.py [-l] [-f FILENAME] [-d DEVICE] [-r SAMPLERATE] [-m MODEL]
```

### Opciones

- `-l, --list-devices`   Muestra la lista de dispositivos de audio disponibles y sale.
- `-f, --filename`       Especifica un archivo donde se guardará la grabación.
- `-d, --device`         Selecciona el dispositivo de entrada de audio (ID numérico o nombre).
- `-r, --samplerate`     Define la tasa de muestreo del audio (opcional, se autodetecta si no se especifica).
- `-m, --model`         Especifica la ruta del modelo de idioma Vosk a utilizar (por defecto: `vosk-model-small-es-0.42`).

### Ejemplos de uso

- Para listar los dispositivos de audio disponibles:
  ```sh
  python script.py --list-devices
  ```

- Para ejecutar el reconocimiento de voz con un dispositivo y guardar la grabación:
  ```sh
  python script.py -d 1 -f audio.raw -m vosk-model-small-es-0.42
  ```

## Notas

- Para detener la grabación, presiona `Ctrl + C`.
- Asegúrate de proporcionar la ruta correcta al modelo de idioma descargado.



