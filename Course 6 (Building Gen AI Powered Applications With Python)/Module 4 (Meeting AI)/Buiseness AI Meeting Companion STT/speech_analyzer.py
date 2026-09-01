import warnings
warnings.filterwarnings("ignore")

import gradio as gr
from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

#######------------- 1. Local LLM Setup (Flan-T5) -------------#######
# Load local text generation pipeline
llm_pipe=pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_new_tokens=512,
    model_kwargs={"temperature":0.3, "do_sample":True}
)

# LangChain local LLM wrapper 
llm = HuggingFacePipeline(pipeline=llm_pipe)

temp = """Summarize and list the key points with details from the following transcript:

Transcript: {context}

Key Points:
"""

pt = PromptTemplate(
    input_variables=["context"],
    template=temp
)
summary_chain = LLMChain(llm=llm, prompt=pt)

#######------------- 3. Speech-to-Text Pipeline (Whisper) -------------#######
# Initialize STT pipeline globally once so it runs fast
stt_pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny.en",
    chunk_length_s=30,
)

def transcript_audio(audio_file):
    if audio_file is None:
        return "Please Upload An Audio File"
    
    # 1. Transcribe speech to text locally using Whisper
    transcript_txt = stt_pipe(
        audio_file, batch_size=8)["text"]

    # 2. Analyze & summarize the transcript with local LLM
    result = summary_chain.run(transcript_txt)

    return f"**Transcript**\n{transcript_txt}\n\n**Summary**\n{result}"

#######------------- 4. Gradio Interface -------------#######
audio_input = gr.Audio(sources=["upload"], type="filepath", label="Upload Meeting / Speech Audio")
output_text = gr.Textbox(label="AI Analysis Output", lines=10)
iface = gr.Interface(
    fn=transcript_audio,
    inputs=audio_input,
    outputs=output_text,
    title="Business AI Meeting Companion & Speech Analyzer",
    description= "Upload an audio file to transcribe it with Whisper and extract key points using a local LLM."
)
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860) 
