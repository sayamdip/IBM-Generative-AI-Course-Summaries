# Encoder-Decoder Based Model Is Used
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/blenderbot-400M-distill"

# Load model (download on first run and reference local installation for subsequent runs)

model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Keeping track of conversation history
conversation_history= []

# Let's print a simple message which will help you to quit the chatbot once the whole code is ready:

print("Chatbot Ready! (type 'exit' to quit)\n")

while True:
    # Encoding the conversation history
    history_string = "\n".join(conversation_history)

    # Fetch prompt from user
    input_text = input("> ")

    # Exit condition
    if input_text.lower() == "exit":
        print("Goodbye!")
        break

    # Tokenization of user prompt and chat history

    prompt = history_string + f"\nUser: {input_text}\nBot:"
    inputs = tokenizer( #tokenizer(...): Converts raw text into numerical tokens the model can understand.
        prompt, 
        return_tensors="pt", # return_tensors="pt": Specifies that PyTorch tensors should be returned.
        truncation=True, # truncation=True: Ensures that inputs longer than the model's maximum length are truncated.
        max_length=512 # Maximum number of tokens allowed as input.
    )

    # Generate output from the model 
    # This Will Be Same Across All Hugging Face Models
    outputs = model.generate(
        **inputs, # Sends the user message and chat history to the model. This helps the chatbot understand the full conversation before replying.
        max_new_tokens= 60, # Limits the length of the chatbot's response to 60 tokens.
        no_repeat_ngram_size=3, # Prevents the model from repeating the same phrase (3-word sequences) to avoid repetitive responses.
        repetition_penalty=1.3, # Penalizes repeating words, making the chatbot speak more naturally.
        do_sample=True, # Enables sampling instead of deterministic generation, adding randomness.
        temperature=0.6, # Controls the randomness of the output. Lower values make the response more predictable; higher values make it more creative.
        top_p=0.85
    )

    # Decode output
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip() 
    # tokenizer.decode(outputs[0]): Converts the model's output from numbers (tokens) back into readable text. The model first generates numbers, and this step turns them into a human-readable sentence.
    # outputs[0]: Takes the first generated response from the model (since the model can generate multiple outputs internally).
    # skip_special_tokens=True: Removes special tokens like padding or system symbols so they don't appear in the final output.
    # .strip(): Removes extra spaces at the beginning and end of the text for a clean output.
    # print(response): Displays the final chatbot reply in the terminal so the user can see it.

    print(response)

    # Update conversation history
    conversation_history.append(f"User: {input_text}")
    conversation_history.append(f"Bot: {response}")
    # print(conversation_history)
