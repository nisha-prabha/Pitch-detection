import numpy as np
from pydub import AudioSegment
import io
import scipy.io.wavfile as wav
import os

def autocorrelation_pitch(signal, fs):
    
    autocorr = np.correlate(signal, signal, mode='full')
    

    autocorr = autocorr[len(autocorr)//2:]
    
    
    peak_index = np.argmax(autocorr[1:]) + 1
    
    
    pitch_freq = fs / peak_index
    
    return pitch_freq

def load_audio(file_path):
    
    try:
    
        if not os.path.exists(file_path):
            raise FileNotFoundError
        
        audio = AudioSegment.from_mp3(file_path)
        with io.BytesIO() as wav_data:
            audio.export(wav_data, format="wav")
            wav_data.seek(0)
            fs, audio_data = wav.read(wav_data)
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)  
        return fs, audio_data
    except FileNotFoundError:
        print("Error: File not found.")
        exit()


if __name__ == "__main__":
    
    file_path = input("Enter the path to the MP3 audio file: ")
    
    
    fs, audio_data = load_audio(file_path)
    
    
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    
    
    pitch_freq = autocorrelation_pitch(audio_data, fs)
    
    print("Estimated Pitch Frequency:", pitch_freq, "Hz")