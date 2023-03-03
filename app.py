from flask import Flask, render_template, request, jsonify
import openai
import os
import dotenv


from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the Flask app
app = Flask(__name__)

# Configure OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")

def gen_prompt(job_description, duration, skills):
    base_prompt = f""" 
    # Given a job title of {job_description}'
    # Given a job length of '{duration}'
    # Given job skills of {skills}
    # Write a detailed job description, without a title
    ## Ask the candidate to submit a proposal
    ## The candidate's should describe how they can help with the project
    ## The candidate should include some links to past completed projects
    """
    return base_prompt

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

        # Return the job description as JSON
        return jsonify({'job_description': job_description})

    # If the request method is GET, render the home page template
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run()

    
