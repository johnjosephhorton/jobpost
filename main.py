
from flask import Flask, render_template, request, jsonify
import openai
import os
import dotenv
import random
import json 

from replit import db

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the Flask app
app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

if db:
  if "generations" not in db.keys():
    db['generations'] = json.dumps([])

    if "modifications" not in db.keys():
      db['modifications'] = json.dumps([])
  
def gen_prompt(job_description, duration, skills):
    base_prompt = f""" 
    # Given a job title of {job_description}'
    # Given a job length of '{duration}'
    # Given job skills of {skills}
    # Write a detailed job description, without a title
    """
    return base_prompt


def modify_job_description(action, job_description):
    response = openai.Edit.create(
        model="text-davinci-edit-001",
        input=job_description,
        instruction=f"Take this job description and {action}.",
        temperature=0.2,
        top_p=1
    )
    new_job_description = response.choices[0].text
    return new_job_description

@app.route('/modify', methods = ['POST'])
def modify():
    print("getting here")
    print(request.form)
    if request.method == 'POST':
        job_description = request.form['job_description']
        action = request.form['action']
        new_job_description = modify_job_description(action, job_description)

        if db:
          data = {'job_description': job_description, 
                  'action': action, 
                  'new_job_description': new_job_description}
          old_data = json.loads(db['modifications'])
          old_data.append(data)
          db['modifications'] = json.dumps(old_data)
          
    return jsonify({'job_description': new_job_description})

# Define the home page route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the job title from the form data
        job_title = request.form['job_title']
        skills = request.form['skills']
        duration = request.form['duration']

        # Call the OpenAI API to generate a job description
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=gen_prompt(job_title, skills, duration),
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Get the generated job description from the API response
        job_description = response.choices[0].text

        if db:
          data = {'job_title': job_title,'skills': skills, 
                'duration': duration, 
                'job_description': job_description}
          
          old_data = json.loads(db['generations'])
          old_data.append(data)
          db['generations'] = json.dumps(old_data)

        # Return the job description as JSON
        return jsonify({'job_description': job_description})

    # If the request method is GET, render the home page template
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug = True, # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	 )

    
