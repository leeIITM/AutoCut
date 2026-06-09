import gradio as gr
from main import process_video


def run_autocut(video):

    if video is None:
        return None

    output_video = process_video(video)

    return output_video


with gr.Blocks(title="AutoCut") as app:

    gr.Markdown("# AutoCut")
    gr.Markdown("Upload a video and get the edited version.")

    with gr.Row():

        input_video = gr.Video(
            label="Input Video"
        )

        output_video = gr.Video(
            label="Edited Video"
        )

    process_btn = gr.Button("Process")

    process_btn.click(
        fn=run_autocut,
        inputs=input_video,
        outputs=output_video
    )

app.launch()