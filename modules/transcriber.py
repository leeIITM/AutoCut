import whisper


class Transcriber:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, video_path):
        result = self.model.transcribe(video_path)

        return {
            "text": result["text"],
            "segments": result["segments"]
        }