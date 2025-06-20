import sounddevice as sd
import soundfile as sf
import numpy as np

def record_audio(filename, duration, fs=44100):
   """
   Record audio for a specified duration and save it to a .wav file.

   :param filename: Name of the output .wav file.
   :param duration: Duration of the recording in seconds.
   :param fs: Sampling frequency (default is 44100 Hz).
   """
   print(f"Recording for {duration} seconds...")
   # Record audio
   recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
   sd.wait()  # Wait until recording is finished
   print("Recording complete. Saving to file...")

   # Save as .wav file
   sf.write(filename, recording, fs)
   print(f"Audio saved to {filename}")

if __name__ == "__main__":
   output_filename = "output.wav"
   record_duration = 5  # Record for 5 seconds
   record_audio(output_filename, record_duration)
