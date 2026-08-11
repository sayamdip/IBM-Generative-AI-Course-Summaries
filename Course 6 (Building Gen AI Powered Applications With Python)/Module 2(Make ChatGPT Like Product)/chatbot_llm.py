# Decoder Only Chatbot Model Is Used
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import warnings
warnings.filterwarnings("ignore") # suppresses unnecessary Hugging Face warning messages to keep the output cleaner.

model_name = "HuggingFaceTB/SmolLM2-360M-Instruct"

print("Load Model ...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.unk_token
# pad_token: In transformer models, inputs in a batch must often be the same length. 
# Shorter sequences are padded with a special token called the padding token (pad_token). 
# This tells the model which parts of the input are real words and which are filler.

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="cpu", # device_map: Controls where the model runs (e.g., CPU or GPU) and ensures it is correctly loaded on the available device.
    torch_dtype = torch.float32 # torch_dtype: Sets the numerical precision of computations (e.g., float32 or float16) to balance speed, memory usage, and accuracy.
)

# Initialize conversation messages
messages = [
    {
        "role":"system",
        "content":"You are a very friendly and cheerful assistant. Always respond in a warm, casual, and encouraging tone."

        # messages: This is the full conversation history between the user and the AI. 
        # Each message has two parts: role, who is speaking and content, what they are saying
    }
]

# Start chatbot loop
print("Chatbot Started. Type 'exit' To Quit\n")
while True:
    user_input = input("> ")

    if user_input.lower() == "exit":
        print("Goodbye")
        break

    # Update conversation history
    messages.append({"role":"user", "content":user_input})

    # To avoid very long conversations, keep only recent exchanges
    messages = [messages[0]] + messages[-10:]

    # Apply chat template
    tokenized = tokenizer.apply_chat_template( 
        # apply_chat_template(): This function converts the structured message format (system, user, assistant) into a single properly formatted prompt that the model can understand. 
        # It ensures the conversation follows the model’s expected template, including special tokens and structure.
        messages, 
        tokenize=True, # tokenize: converts text into tokens
        add_generation_prompt=True, # signals the model to generate a reply This flag tells the model that the input ends here and it should now start generating a response. 
                                    # It ensures the model knows where the assistant’s reply should begin in the conversation format. 
        return_tensors="pt", # return_tensors: Specifies the format of the output, ensuring it is ready for PyTorch operations.
        return_dict=True, # return_dict: Configures the output to be returned as a dictionary, which is useful for accessing different parts of the model's output (like hidden states or attentions).
        max_length=512
    )

    # Generate response
    with torch.inference_mode(): # Runs the code in inference mode (no training). It makes generation faster and memory-efficient.
        outputs = model.generate( # This is the function that actually makes the model produce a response based on the input tokens.
            tokenized["input_ids"], # input_ids: These are the numerical IDs of the tokens.
            attention_mask=tokenized["attention_mask"], # attention_mask: This mask tells the model which tokens are real and which are padding.
            max_new_tokens=60, # Limits the length of the chatbot's response to 60 tokens.
            temperature=0.5, # Controls the randomness of the output. Lower values make the response more predictable; higher values make it more creative.
            top_p=0.8, # Controls the diversity of the output. Lower values make the response more predictable; higher values make it more creative.
            do_sample=True, # Enables sampling instead of deterministic generation, adding randomness.
            repetition_penalty=1.3, # Penalizes repeating words, making the chatbot speak more naturally.
            no_repeat_ngram_size=3, # Prevents the model from repeating the same phrase (3-word sequences) to avoid repetitive responses.
            pad_token_id=tokenizer.pad_token_id # pad_token_id: The ID of the token used for padding (making sequences the same length).
        )

    # Decode and display response
    response = tokenizer.decode(
        outputs[0][tokenized["input_ids"].shape[-1]:], # This part extracts only the newly generated response from the model.
        # outputs[0] :full sequence (input + generated text)
        # tokenized["input_ids"].shape[-1] : Length of the input tokens
        skip_special_tokens=True
    )

    print(f"Bot: {response}\n")

    # Update conversation history
    messages.append({"role":"assistant","content":response})






