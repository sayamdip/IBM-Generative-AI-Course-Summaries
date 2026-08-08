import gradio as gr
import os

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
)
port = int(os.environ.get("PORT", 8080))

demo.launch(server_name="0.0.0.0", server_port=port)

