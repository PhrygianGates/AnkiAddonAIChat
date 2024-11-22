import subprocess
import re

class AudioRecorder:
    def __init__(self):
        self.output_file = "output.m4a"

    def start_recording(self):
        try:
            # Start recording using ffmpeg with silence detection to automatically stop recording
            process = subprocess.Popen([
                "ffmpeg", "-y", "-f", "avfoundation", "-i", ":0", "-ar", "44100",
                "-ac", "1", "-b:a", "128k", "-af", "silencedetect=noise=-50dB:d=3",
                self.output_file
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            silence_pattern = re.compile(r"silencedetect")
            while True:
                output = process.stderr.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    if silence_pattern.search(output):
                        process.terminate()
                        break
        except FileNotFoundError:
            print("Error: ffmpeg not found. Please ensure it is installed and available in your PATH.")

    def record_and_transcribe(self):
        self.start_recording()

        # Transcribe the recorded file using whisperkit-cli
        try:
            result = subprocess.run([
                "whisperkit-cli", "transcribe",
                "--audio-path", self.output_file,
                "--model-path", "/Users/zhichengx/Library/Containers/com.argmax.whisperkit.WhisperAX/Data/Documents/huggingface/models/argmaxinc/whisperkit-coreml/openai_whisper-large-v3-v20240930_turbo"
            ], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print("Error during transcription:", result.stderr)
                return ""
        except FileNotFoundError:
            print("Error: whisperkit-cli not found. Please ensure it is installed and available in your PATH.")
            return ""

if __name__ == "__main__":
    recorder = AudioRecorder()
    transcription = recorder.record_and_transcribe()
    if transcription:
        print("Transcription:")
        print(transcription)
