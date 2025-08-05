import sounddevice as sd
import soundfile as sf
import numpy as np
import time
from pynput import keyboard
import whisperx
import gc
import torch


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

def transcribe_audio(audio_file):
    # Set device
    if torch.cuda.is_available():
        device = torch.device("cuda")
    # elif torch.backends.mps.is_available():
    #     device = torch.device("mps")
    else:
        device = torch.device("cpu")

    batch_size = 16 # reduce if low on GPU mem
    compute_type = "int8" # "float16" # change to "int8" if low on GPU mem (may reduce accuracy)
    print('loading model')
    # 1. Transcribe with original whisper (batched)
    # model = whisperx.load_model("large-v2", device=device, compute_type=compute_type)
    model = whisperx.load_model("large-v2", 'cpu', compute_type='int8')

    # save model to local path (optional)
    # model_dir = "/path/"
    # model = whisperx.load_model("large-v2", device, compute_type=compute_type, download_root=model_dir)
    print('loading audio')
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size, language='en')
    print('printing transcription\n-----------')
    print(result["segments"][0]['text']) # before alignment

    # delete model if low on GPU resources
    # import gc; import torch; gc.collect(); torch.cuda.empty_cache(); del model

    # 2. Align whisper output
    # model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    # result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    # print(result["segments"]) # after alignment
    return

def format_request():
    return

def speak_reply():
    return

if __name__ == "__main__":
    try:
        while True:
            timestamp = int(time.time())
            output_filename = f"output_{timestamp}.wav"
            record_audio(output_filename)
            transcribe_audio(output_filename) # load recording and transcribe to text file
            # format_request() # append text file to llm conversation history, send api request
            # speak_reply() # convert request response to speech
    except KeyboardInterrupt:
        print("\nRecording loop stopped by user.")