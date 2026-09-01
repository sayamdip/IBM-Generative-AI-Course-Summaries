from transformers import pipeline
from langchain.llms import HuggingFacePipeline

# Load local model (downloads automatically on first run)
pipe = pipeline("text2text-generation", 
                model="google/flan-t5-base",
                max_new_tokens=256,
                model_kwargs={"temperature": 0.3,
                "do_sample":True}
)

# Langchain LLM Wrapper

llm = HuggingFacePipeline(pipeline=pipe)

print(llm("How To Read A Book Effectively?"))