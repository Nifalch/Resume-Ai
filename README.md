Resume AI - Tailored Resume & Cover Letter Generator

A Streamlit web app designed to help users tailor their resumes and generate personalized cover letters. By analyzing job descriptions and resumes, this tool leverages Google's Gemini AI to assess the alignment between the user's profile and the job requirements. It also calculates ATS (Applicant Tracking System) scores to improve job application success.

Features

Job Description Analysis: Input job descriptions to understand key skills and requirements.
Resume Upload: Upload a PDF resume for analysis.
Resume Tailoring: Generate a tailored resume that matches the job description.
ATS Score: Evaluate the resume's compatibility with job requirements and provide a match percentage along with missing keywords.
Cover Letter Generation: Automatically generate a personalized cover letter based on the job description and resume.
Technology Stack

Frontend: Streamlit
Backend: Python
AI Model: Google Gemini AI
Libraries:
pdf2image - To convert PDF resumes to images for AI analysis.
PIL - For image processing.
google-generativeai - For interacting with Gemini AI.
dotenv - For managing environment variables.
Installation

Clone the repository:
bash
Copy code
git clone https://github.com/yourusername/resume-ai.git
cd resume-ai
Create a virtual environment:
bash
Copy code
python -m venv venv
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Set up environment variables:
Create a .env file in the root directory and add your Google API key:
text
Copy code
GOOGLE_API_KEY=your_api_key
Run the app:
bash
Copy code
streamlit run app.py
How It Works

Job Description: Input the job description to get started. The app will analyze key skills and qualifications.
Upload Resume: Upload your resume in PDF format.
Analyze: The app will generate a detailed analysis of how well your resume matches the job description.
Generate Documents: You can choose to generate a tailored resume or cover letter based on the analysis.
Contributing

If you'd like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request. Please ensure that all code follows PEP 8 standards and include test cases for any new features.

License

This project is licensed under the MIT License - see the LICENSE file for details.
