import argparse
import queue
import sys
import sounddevice as sd
import wave
import json

from vosk import Model, KaldiRecognizer

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to (RAW format)")
parser.add_argument(
    "-t", "--transcription-file", type=str, metavar="TRANSCRIPTION_FILE",
    help="file to store the transcription (TXT format)")
parser.add_argument(
    "-i", "--input-file", type=str, metavar="INPUT_FILE",
    help="audio file to transcribe (WAV format)")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)

try:
    if args.samplerate is None:
        if args.input_file:
            with wave.open(args.input_file, 'rb') as wf:
                args.samplerate = wf.getframerate()
        else:
            device_info = sd.query_devices(args.device, "input")
            args.samplerate = int(device_info["default_samplerate"])

    model_path = "vosk-model-es-0.42"  # Reemplaza esto con la ruta correcta
    model = Model(model_path)

    # Manejo de archivos de salida
    dump_fn = None
    transcription_file = None
    if args.filename:
        dump_fn = open(args.filename, "wb")
    if args.transcription_file:
        transcription_file = open(args.transcription_file, "w", encoding="utf-8")

    if args.input_file:
        # Procesar un archivo de audio
        with wave.open(args.input_file, 'rb') as wf:
            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)
            rec.SetPartialWords(True)
            full_result = ""  # Acumular el resultado completo
            while True:
                data = wf.readframes(128000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if "text" in result:
                        full_result += result["text"] + " "  
                else:
                   partial = json.loads(rec.PartialResult())

            final_result = json.loads(rec.FinalResult())
            if "text" in final_result:
                full_result += final_result["text"] 

        # Guarda la transcripción en un archivo
        if transcription_file:
            transcription_file.write(full_result)
            transcription_file.close()
            print(f"Transcription saved to {args.transcription_file}")

    else:
        # Procesar el micrófono
        with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device,
                               dtype="int16", channels=1, callback=callback):
            print("#" * 80)
            print("Press Ctrl+C to stop the recording")
            print("#" * 80)

            rec = KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                   # print(result)  # Imprime el resultado inmediato
                    if transcription_file:  # Guarda la transcripción en tiempo real
                        transcription_file.write(result + "\n")
                        transcription_file.flush()  # Asegura que se escriba inmediatamente
                else:
                    partial = rec.PartialResult()
                   # print(partial)  # Imprime el resultado parcial
                if dump_fn is not None:
                    dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    print(type(e).__name__ + ": " + str(e))
    parser.exit(1)
finally:
    if dump_fn:
        dump_fn.close()
    if transcription_file:
        transcription_file.close()