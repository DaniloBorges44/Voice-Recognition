import pyaudio as pa
import whisper
import math
import struct
import wave
import time
from pynput.keyboard import Key, Controller

# -- Configuração do ambiente --
keyboard = Controller()
model = whisper.load_model("small") # tiny, base, small, medium, large, turbo
keys = {
    "forward" : "w",
    "backward" : "s",
    "left" : "a",
    "right" : "d",
    "roll" : "Key.space",
    "light" : "h",
    "heavy" : "u",
    "use" : "e",
    "lock" : "o"
}

# iniciando variaveis
FORMAT = pa.paInt16      # Formato do audio
CHANNELS = 1             # Tipo de saida: Mono
RATE = 44100             # Frenquência do audio (Hz)
CHUNK = 1024             # Frames por buffer
FILENAME = 'output.wav'  # Nome do arquivo de saida

def get_volume(stream): # Identifica o volume de cada frame

        data = stream.read(CHUNK)
        # Convert the binary data to a list of numbers
        data_chunk = struct.unpack(str(CHUNK) + 'h', data)

        # Calcula a media da raiz quadrada como o volume
        volume = math.sqrt(sum([x**2 for x in data_chunk]) / len(data_chunk))
        
        return volume
   
def verify_volume(volume): # verifica se o volume é maior que determinado valor
        if volume <= 50:
            return 1
        elif volume <= 150:
            return 2
        elif volume > 150:
            return 3
            
def record_audio(): # Detecta o audio e salva em um arquivo WAV
    try:
        audio = pa.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,frames_per_buffer=CHUNK)

        frames = []

        for i in range(0, int(RATE / CHUNK * 2)):
            data = stream.read(CHUNK)
            frames.append(data)

        wf = wave.open(FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    
    
        return stream

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
    
def detect_comand(stream): # Detecta e realiza o comando falado
    for segment in result["segments"]:
        if segment["text"].lower() in keys:
            match verify_volume(get_volume(stream)):
                case 1:
                    keyboard.press(keys[segment["text"].lower()])
                    time.sleep(0.5) 
                    keyboard.release(keys[segment["text"].lower()])
                case 2:
                    keyboard.press(keys[segment["text"].lower()])
                    time.sleep(1) 
                    keyboard.release(keys[segment["text"].lower()])
                case 3:
                    keyboard.press(keys[segment["text"].lower()])
                    time.sleep(2) 
                    keyboard.release(keys[segment["text"].lower()])
                case _:
                    print("Erro ao realizar ação")
        else:
            break
   
while True: # Loop principal
    try: 
        stream = record_audio()
        audio = whisper.pad_or_trim(whisper.load_audio("output.wav"))
        result = whisper.transcribe(model, audio, fp16=False)
        print(result["text"])
        detect_comand(stream)
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break