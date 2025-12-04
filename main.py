import pyaudio as pa
import whisper
import math
import struct
import wave
import time
from pynput.keyboard import Controller

# -- Configuração do ambiente --
keyboard = Controller()
model = whisper.load_model("small") # tiny, base, small, medium, large, turbo
keys = { # Dicionario com os comandos e teclas correspondentes 
    "forward" : "w",
    "backward" : "s",
    "left" : "a",
    "right" : "d",
    "roll" : "Key.space",
    "light" : "h",
    "heavy" : "u",
    "use" : "e",
    "lock" : "o",
    "thank you." :"y"
}

# iniciando variaveis
FORMAT = pa.paInt16      # Formato do audio
CHANNELS = 1             # Tipo de saida: Mono
RATE = 16000             # Frenquência do audio (Hz)
CHUNK = 1024             # Frames por buffer
FILENAME = 'output.wav'  # Nome do arquivo de saida

def get_volume(stream): # Identifica o volume de cada frame
    data = stream.read(CHUNK)
    data_chunk = struct.unpack(str(CHUNK) + 'h', data)
    volume = math.sqrt(sum([x**2 for x in data_chunk]) / len(data_chunk))
        
    return volume
   
def verify_volume(volume): # verifica se o volume é maior que determinado valor
    if volume <= 50:
        return 1
    elif volume <= 150:
        return 2
    elif volume > 150:
        return 3
        
def process_audio(): # Processa o audio capturado 
    try:
        audio = pa.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,frames_per_buffer=CHUNK)
        
        frames = []
        
        for i in range(0, int(RATE / CHUNK * 1)): # Salva os frames do audio, ultimo numero é o tempo que ele capta o audio
            data = stream.read(CHUNK)
            frames.append(data)
            
        # -- Salva os dados no arquivo de audio --
        wf = wave.open(FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        # -- Salva os dados no arquivo de audio --
        
        # -- Transcreve o audio --
        audio_data = whisper.pad_or_trim(whisper.load_audio("output.wav"))
        result = whisper.transcribe(model, audio_data, fp16=False)
        print("Fala detectada: " + result["text"].lstrip())
        # -- Transcreve o audio --
        
        detect_comand(result, stream)
    
    except Exception as e:
        print(f"Erro ao processar áudio: {e}")

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

def detect_comand(result, stream): # Detecta e realiza o comando falado
    for segment in result["segments"]:
        text = segment["text"].lower().lstrip()
        
        if keys.get(text):
            volume = verify_volume(get_volume(stream))
            press_time = {1: 0.5, 2: 1, 3: 2}.get(volume, 0.5) # Dicionario que relaciona o volume com o tempo precionado
            print(f"Tecla pressionada: {keys[text]}")
            keyboard.press(keys[text])
            time.sleep(press_time)
            keyboard.release(keys[text])
            
        else:
            break

while True: # Loop principal
    try: 
        process_audio()
        time.sleep(0.1) # sleep para evitar erros      
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break