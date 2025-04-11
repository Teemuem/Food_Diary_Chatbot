# ai_utils.py
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

# Function to initialize the language model (LLM)
def initialize_llm():
    # Load environment variables from a .env file
    load_dotenv(override=True)
    
    # Retrieve the Ollama server URL from the environment variables
    OLLAMA_SERVER_URL = os.environ["OLLAMA_SERVER_URL"]
    
    # Create an instance of the OllamaLLM with model "llama3.2" and the specified server URL
    llm = OllamaLLM(model="llama3.2", base_url=OLLAMA_SERVER_URL)
    
    # Return the initialized language model instance
    return llm

# Function to create an LLM chain using a prompt template
def create_chain(llm):
    # Open and read the template file (template.txt)
    with open('template.txt', 'r') as file:
        template = file.read()
    
    # Create a prompt template using the contents of template.txt
    prompt_template = ChatPromptTemplate.from_template(template)
    
    # Create an LLMChain using the prompt template and the provided language model (llm)
    chain = LLMChain(prompt=prompt_template, llm=llm)
    
    # Return the LLMChain instance
    return chain