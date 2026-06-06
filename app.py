import gradio as gr

from main import process_video


def autocut(video):

    if video is None:
        return None

    output_video = process_video(video)

    return output_video


with gr.Blocks(title="AutoCut") as demo:

    gr.Markdown(
        "# AutoCut\n"
        "Upload a video and get an edited version."
    )

    with gr.Row():

        input_video = gr.Video(
            label="Input Video"
        )

        output_video = gr.Video(
            label="Processed Output"
        )

    process_btn = gr.Button(
        "Process Video"
    )

    process_btn.click(
        fn=autocut,
        inputs=input_video,
        outputs=output_video
    )

demo.launch()