import sys
import whisper

class Transcriber:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, video_path):
        result = self.model.transcribe(
            video_path,
            word_timestamps=True
        )

        return {
            "text": result["text"],
            "segments": result["segments"]
        }


if __name__ == "__main__":

    video_path = sys.argv[1]

    transcriber = Transcriber()

    transcript = transcriber.transcribe(video_path)

    print(transcript["segments"][0])