from flask import Flask, render_template, request
import schedule
import time
import threading
import subprocess

app = Flask(__name__)


def call_initiate(prompt_of_user, intention):

    cmd = ["python3", "initiate.py", prompt_of_user, intention]
    # Execute the command
    subprocess.run(cmd)

# Function to be executed for posting
def post(prompt_of_user, intention, tenure):
    message = f"Successfully posted about {prompt_of_user} with {intention} on your LinkedIn.\n"
    if tenure != "Single Post":
        message += f"Remaining posts will be initiated at 8 AM every morning for {tenure - 1} days on your LinkedIn."
    print(message)
    # Call initiate.py to perform the posting
    call_initiate(prompt_of_user, intention)
    return message

# Function to handle scheduling
def schedule_posting(prompt_of_user, intention, days):
    # Post immediately
    message = post(prompt_of_user, intention, days)
    
    if days > 1:
        # Schedule remaining posts for every day at 8 AM
        for i in range(1, days):
            schedule.every(i).days.at("08:00").do(post, prompt_of_user, intention, days)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/automate', methods=['POST'])
def process():
    prompt_of_user = request.form['prompt_of_user']
    intention = request.form['intention']
    post_tenure = request.form['post_tenure']

    # Process the data as needed
    # For now, just print it
    print("Prompt of User:", prompt_of_user)
    print("Intention:", intention)
    print("Post Tenure:", post_tenure)

    if post_tenure != "Single Post":
        days = int(post_tenure.split()[0])
        # Schedule posting
        schedule_posting(prompt_of_user, intention, days)
        return f"Successfully posted about {prompt_of_user} with {intention} on your LinkedIn.\nRemaining posts will be initiated at 8 AM every morning for {days - 1} days on your LinkedIn."
    else:
        
        message = post(prompt_of_user, intention, post_tenure)
        return message

def schedule_run():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':

    scheduling_thread = threading.Thread(target=schedule_run)
    scheduling_thread.start()
    
    app.run(debug=True)
