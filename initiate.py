import os
import sys
import subprocess

python_file='textai.py'

if len(sys.argv) < 3:
    print("Usage: python script.py <prompt> <intention>")
    sys.exit(1)
    

prompt = sys.argv[1]
intention = sys.argv[2]

subprocess.run(["python3", python_file, prompt,intention])


