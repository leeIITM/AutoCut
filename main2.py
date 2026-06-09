import sys
from modules.transcriber import transcriber
from modules.ass_generator import generate_ass
from modules.silence import remove_silence


'''def main():

    if len(sys.argv) < 2:
        print("Usage: python main.py <video_path>")
        return

    video_path = sys.argv[1]

    transcriber = Transcriber()

    result = transcriber.transcribe(video_path)

    generate_ass(
        result["segments"],
        "./output/subtitles.ass"
    )


if __name__ == "__main__":
    main()'''

def process_video(video_path):

    edited_video = remove_silence(video_path)

    transcript = transcriber.transcribe(
        edited_video
    )

    generate_ass(
        transcript["segments"],
        "temp.ass"
    )

    final_video = burn_subtitles(
        edited_video,
        "temp.ass"
    )

    return final_video