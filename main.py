from RealtimeSTT import AudioToTextRecorder


def process_text(text):
    print(text)


if __name__ == "__main__":
    recorder = AudioToTextRecorder(language="pt", device="cpu")

    while True:
        recorder.text(process_text)



'''import pyaudio as pa
import whisper
import wave
import time
from pynput.keyboard import Controller

# -- Configuração do ambiente --
keyboard = Controller()
model = whisper.load_model("small") # tiny, base, small, medium, large, turbo

# iniciando variaveis
FORMAT = pa.paInt16      # Formato do audio
CHANNELS = 1             # Tipo de saida: Mono
RATE = 44100             # Frenquência do audio (Hz)
CHUNK = 1024             # Frames por buffer
FILENAME = 'output.wav'  # Nome do arquivo de saida
        
def process_audio(): # Processa o audio capturado 
    try:
        audio = pa.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        
        frames = []
        
        for i in range(0, int(RATE / CHUNK * 10)): # Salva os frames do audio, ultimo numero é a duração do audio
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
        audio_data = whisper.load_audio("output.wav")
        result = whisper.transcribe(model, audio_data, fp16=False)
        print("Fala detectada: " + result["text"].lstrip())
        # -- Transcreve o audio --
        
    except Exception as e:
        print(f"Erro ao processar áudio: {e}")

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

while True: # Loop principal
    try: 
        process_audio()
        time.sleep(0.1) # sleep para evitar erros      
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break'''