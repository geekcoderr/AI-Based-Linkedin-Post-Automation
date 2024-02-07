import textwrap
import os
import sys
import subprocess
from google.generativeai import generative_models
from dotenv import load_dotenv
from IPython.display import display
from IPython.display import Markdown
import google.generativeai as genai
python_file='autoPostLinkedin.py'

# Load environment variables from .env file
load_dotenv()

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ')
# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')


if len(sys.argv) < 3:
    print("Usage: python script.py <prompt> <intention>")
    sys.exit(1)

prompt = sys.argv[1]
intention = sys.argv[2]
final_prompt = f"Start with a good heading and hastags , {prompt} with Intention as {intention}, see this is to be posted on linkedin so genarate in that format with real hastags placed appropriately"

response = model.generate_content(final_prompt)
print(to_markdown(response.text))
subprocess.run(["python3", python_file, response.text])

