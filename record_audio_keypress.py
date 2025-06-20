import sounddevice as sd
import soundfile as sf
import numpy as np
import time
from pynput import keyboard

def record_audio(filename, fs=44100):
    """
    Records audio while spacebar is pressed. Saves only if pressed >= 0.5 seconds.

    :param filename: Name of the output .wav file.
    :param fs: Sampling frequency (default is 44100 Hz).
    """
    print("Press and hold the spacebar to record. Release to stop.")
    audio_data = []
    is_recording = [True]
    start_time = [None]

    def on_press(key):
        if key == keyboard.Key.space:
            if start_time[0] is None:
                start_time[0] = time.time()  # Record when spacebar is pressed

    def on_release(key):
        if key == keyboard.Key.space:
            is_recording[0] = False  # Stop recording

    # Set up keyboard listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # Start recording
    with sd.InputStream(samplerate=fs, channels=2, dtype='float32') as stream:
        stream.start()
        while is_recording[0]:
            data, overflowed = stream.read(1024)
            if overflowed:
                print("Warning: Audio buffer overflowed")
            audio_data.append(data.copy())
        stream.stop()

    # Calculate duration
    if start_time[0] is not None:
        duration = time.time() - start_time[0]
        if duration >= 0.5 and len(audio_data) > 0:
            print("Saving to file...")
            recording = np.concatenate(audio_data, axis=0)
            sf.write(filename, recording, fs)
            print(f"Audio saved to {filename}")
        else:
            print(f"KeyPress too short ({duration:.2f}s). No audio saved.")
    else:
        print("No valid key press detected.")

if __name__ == "__main__":
    try:
        while True:
            timestamp = int(time.time())
            output_filename = f"output_{timestamp}.wav"
            record_audio(output_filename)
    except KeyboardInterrupt:
        print("\nRecording loop stopped by user.")
