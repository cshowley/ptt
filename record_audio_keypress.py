import sounddevice as sd
import soundfile as sf
import numpy as np
import time
from pynput import keyboard

def record_audio(filename, fs=44100):
    """
    Records audio only while Right Shift is pressed. Saves only if held ≥ 0.5 seconds.
    """
    print("Press and hold Right Shift (Shift_R) to record. Release to stop.")
    audio_data = []
    is_recording = [False]
    start_time = [None]

    def on_press(key):
        if key == keyboard.Key.shift_r:
            is_recording[0] = True
            start_time[0] = time.time()

    def on_release(key):
        if key == keyboard.Key.shift_r:
            is_recording[0] = False

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # Wait for Right Shift to be pressed
    while not is_recording[0]:
        time.sleep(0.01)

    # Start audio capture only after Right Shift is pressed
    with sd.InputStream(samplerate=fs, channels=2, dtype='float32') as stream:
        stream.start()
        print("Recording...")

        while is_recording[0]:
            data, overflowed = stream.read(1024)
            if overflowed:
                print("Warning: Audio buffer overflowed")
            audio_data.append(data.copy())

        stream.stop()

    # Finalize and save if duration is sufficient
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