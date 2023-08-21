import gradio as gr

def greet(src_path_list, dst_path_list, ref_path, work_dir, if_BuildOverviews):

    return 0, 0

demo = gr.Interface(
    fn=greet,
    inputs=["text", "text", "text", "text", "checkbox"],
    outputs=["text", "number"],
)
demo.launch()