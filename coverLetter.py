import openai
import os

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    print("API key not found. Please set the OPENAI_API_KEY environment variable.")
    exit(1)

def generate_cover_letter(position_requirements, your_experiences, job_location):
    prompt = f"""
    Write a cover letter for the position with the following requirements:\n
    {position_requirements}\n\n
    Based on my experiences:\n
    {your_experiences}\n\n
    The job location is {job_location}. Make sure to highlight relevant skills and accomplishments.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Example usage
position_requirements = """
College or University diploma/degree in Television Broadcasting
Minimum of 3 years of Lighting Technician experience
Working knowledge of both LED and Incandescent fixtures and their respective applications
General knowledge of the entire production chain
Time management skills
"""

your_experiences = """
5S Subject Matter Expert, Johnson Electronic (Ancaster Ontario Canada)    
    January 2024 – Currently 
    • Initiates and manages 5S projects, leading meetings to ensure adherence to timelines. 33.206 Shop Floor walls cleaned, 70% of light fixtures replaced in the Shop Floor, 6 200 Ton CINCINNATI compacting presses cleaned, 1 200 TON CINCINNATI coining press cleaned, 4 36" long sinter furnaces cleaned, 7 new racks installed in the shop floor.
    • Responsible for developing 5S audits & scheduling along with improving the auditing system. 89 audits conducted.
    • Develops visual management standards for Defines, modifies and maintains 5S procedures and 5S standards. 3 standards updated.
    • Understanding the leak repair system and able to coach employees. 74 leak work orders followed up until completed.
    • Works with vendors as it relates to projects along with obtaining quotes & submitting purchase orders. New rack quote approved, 3 wall side quotes approved, 7k CAD steamer cleaned and vacuum machine procured, 4 quotes for outsourcing electrical installation approved, 3 quotes for light fixture replacement approved.
    • Works in conjunction with Focus Factory Leaders (FFL) to institute standard 5S practices. 5S blitz program initiated.

Set-Up, Stackpole/Johnson Electronic (Ancaster Ontario)        
    October 2023 - January 2024
    • Track data associated with production equipment. Report any inconsistencies.
    • Write and/or modify CNC programs for lathes, milling machines, and grinders
    • Set up CNC lathes, milling machines, grinders, SPM’s based on process specifications.
    • Analyze “out of tolerance" conditions and make adjustments via offsets.
    • Read and interpret CMM reports.
    • Identify, select and prepare tooling.
    • Process and tooling improvements for cost reduction programs i.e. analyze tool wear and modify programs to improve tooling cost.
    • Work in compliance with Stackpole FPS Quality Systems, Safety Systems & Environmental Systems

Production Associate, Stackpole/Johnson Electronic (Ancaster Ontario)  
    August 2023 - October 2023

Senior Software Engineer, Warner Brothers (Chile/Toronto)              
    April 2022 - Present
    • Creating applications to deliver sport content to end users on different screens: Tozen, iOS, AndroidTV, Android and Web (React.js, TypeScript, Apollo GraphQL)
    • Creating data pipelines to export data from Mongo to Dalton (Python, AWS-Lambda, AWS-S3, AWS-DynamoDB, Terraform CD-CI) 
    • Adding value to the current offering in terms of adding new payment options, new provider enrollment - BTB, creating containers for every country's laws.
    • Working with different departments around the globe to develop the sport vertical.
"""

job_location = "Crossroads in Burlington, ON L7P 0V5"

output = generate_cover_letter(position_requirements, your_experiences, job_location)
print(output)
