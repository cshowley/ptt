import sounddevice as sd
import soundfile as sf
import numpy as np
import time
from pynput import keyboard

def record_audio(filename, fs=44100):
    """
    Record audio on keypress (spacebar) and stop on release.
    """
    print("Press and hold the spacebar to record. Release to stop.")
    audio_data = []
    is_recording = [True]  # Mutable flag to share across scopes

    def callback(indata, frames, time_info, status):
        if status:
            print(f"Status: {status}")
        if is_recording[0]:
            audio_data.append(indata.copy())

    listener = keyboard.Listener(
        on_press=lambda key: None,  # Not used here
        on_release=lambda key: is_recording.__setitem__(0, False) if key == keyboard.Key.space else None
    )
    listener.start()

    with sd.InputStream(samplerate=fs, channels=2, dtype='float32', callback=callback):
        while is_recording[0]:
            time.sleep(0.1)  # Non-blocking wait

    print("Saving to file...")
    recording = np.concatenate(audio_data, axis=0)
    sf.write(filename, recording, fs)
    print(f"Audio saved to {filename}")

if __name__ == "__main__":
    try:
        while True:
            timestamp = int(time.time())
            record_audio(f"output_{timestamp}.wav")
    except KeyboardInterrupt:
        print("\nRecording loop stopped by user.")
