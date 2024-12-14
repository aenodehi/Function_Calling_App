import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv
import os
import torch

# Load environment variables from the .env file
load_dotenv()

# Get Hugging Face API token from the .env file
hf_api_token = os.getenv("HF_TOKEN")
if not hf_api_token:
    st.error("Hugging Face API token not found in the .env file.")
    st.stop()

# Model name
# model_name = "LiteLLMs/Mistral-Nemo-Instruct-2407"  # Update this to your model name
model_name = "mistralai/Mistral-Nemo-Instruct-2407"  # Update this to your model name

# Ensure PyTorch is installed and check if GPU is available
if not torch.cuda.is_available():
    st.warning("GPU is not available. The model may run slowly on CPU.")

try:
    # Load tokenizer and model with authentication
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_api_token)
    model = AutoModelForCausalLM.from_pretrained(model_name, token=hf_api_token)
    llm_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, token=hf_api_token)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Streamlit input
prompt = st.text_input("Enter your prompt")

if prompt:
    # Generate response using the Hugging Face model
    try:
        response = llm_pipeline(prompt, max_length=150, num_return_sequences=1)[0]["generated_text"]
    except Exception as e:
        st.error(f"Error generating response: {e}")
        response = None

    # Display AI response
    if response:
        st.write(response)


