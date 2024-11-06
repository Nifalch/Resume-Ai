import streamlit as st
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Helper function to convert PDF to image
import fitz  # PyMuPDF

def convert_pdf_to_image(pdf_file):
    # Open the provided PDF file
    doc = fitz.open(pdf_file)
    
    # Loop through all the pages (for now, we'll convert only the first page)
    page = doc.load_page(0)  # 0 is the first page
    pix = page.get_pixmap()  # Convert page to a pixmap (image)
    
    # Save the pixmap as a PNG image
    image = pix.tobytes("png")  # Converts to PNG in bytes
    
    return image

# Example of using the function with the uploaded file
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
if uploaded_file is not None:
    pdf_content = convert_pdf_to_image(uploaded_file)
    st.image(pdf_content)  # Display the image in Streamlit


# AI model function
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Streamlit App Config with Custom Favicon
st.set_page_config(
    page_title="Resume Ai",
    page_icon="logo.png",  
    layout="centered"
)

# Custom CSS for Modern UI
st.markdown("""
    <style>
    /* App background color */
    .app-background {
        background-color: #F8F9FA;
        color: #333;
    }

    /* Header and Logo */
    .header-logo img {
        display: block;
        margin: 0 auto;
        width: 150px;  /* Adjust the width as needed */
        margin-bottom: 10px;
        border-radius: 10%;
    }
    
    /* Green button styling */
    .stButton>button {
        background: #28a745;
        color: white;
        border-radius: 8px;
        padding: 35px 20px;
        font-weight: bold;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        border: none;
        height: 50px; /* Fixed height for buttons */
    }
    
    .stButton>button:hover {
        background-color: white;
        color: black;
    }
    
    /* File upload area */
    .upload-area {
        border: 2px dashed #28a745;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: #333;
    }
    
    /* Input fields */
    textarea, .stTextInput input {
        background-color: #F0F0F0;
        color: #333;
        border-radius: 10px;
        border: 1px solid #ccc;
        padding: 10px;
    }
    
    /* Subheaders */
    .stSubheader {
        color: #333;
        font-size: 22px;
        font-weight: 600;
    }

    /* Footer */
    .footer {
        font-size: 14px;
        color: #666;
        text-align: center;
        padding: 10px 0;
    }
    
    .footer a {
        color: #28a745;
        text-decoration: none;
        font-weight: bold;
    }
    
    .footer a:hover {
        color: #218838;
    }

    /* Equal height for all columns with buttons */
    .button-column {
        display: flex;
        justify-content: space-around;
        align-items: stretch;
    }
    
    </style>
""", unsafe_allow_html=True)

# Logo Section - Make sure the logo image is in the same directory as the app file or provide the correct relative path
logo_path = "aire.png"  
if os.path.exists(logo_path):
    # Center the logo using Markdown and HTML
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image(logo_path, width=250)  
    st.markdown("</div>", unsafe_allow_html=True)

# Job Description Input Section
st.subheader("Job Description")
input_text = st.text_area("Enter the Job Description", placeholder="Paste the job description here...", key="input" )

# Resume Upload Section
st.markdown("<div class='upload-area'>Upload your resume (PDF only)</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["pdf"])

# Action Buttons in the same row with separate buttons for Resume and Cover Letter
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])  # Adjust the width for each button column
with col1:
    analyze_button = st.button("Analyze Resume")
with col2:
    match_button = st.button("ATS Score")
with col3:
    generate_cover_letter_button = st.button("Generate Cover Letter")
with col4:
    generate_resume_button = st.button("Generate Tailored Resume")

# Prompts
input_prompt1 = """
As an experienced HR Manager, review the provided resume against the job description.
Assess how well the candidate’s profile aligns with the role, noting key strengths and areas for improvement.
"""

input_prompt3 = """
As a skilled ATS system, evaluate the resume based on the job description.
Provide a match percentage(ATS Score), list missing keywords, and share an overall assessment.
"""

input_prompt_cover_letter = """
Based on the job description and my uploaded resume, create a professional, three-paragraph cover letter. In the first paragraph, mention the [role] I'm applying for and how I learned about this opportunity. In the second paragraph, highlight my relevant skills, experiences, and accomplishments that align with the job description. In the third and final paragraph, express my enthusiasm for the role, thank the recruiters for their time, and convey my excitement for the next stages of the hiring process.and sincerly [name]
"""

input_prompt_resume = """
Using the provided job description and the uploaded resume, create a tailored resume that best fits the requirements of the job. 
Make sure to highlight the relevant skills, experience(make sure in bullet points), and qualifications from the resume that match the job description. If any areas of improvement or additions are needed, suggest modifications to ensure the resume aligns with the job's key requirements. The tailored resume should showcase the most relevant aspects of the candidate's experience that directly correspond to the role, skills, and qualifications mentioned in the job description.
"""

# Analysis & Response
if analyze_button:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        with st.spinner("Analyzing resume..."):
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("Resume Analysis")
            st.write(response)
    else:
        st.warning("Please upload your resume to proceed.")

elif match_button:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        with st.spinner("Calculating match percentage..."):
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.subheader("Match Percentage & Recommendations")
            st.write(response)
    else:
        st.warning("Please upload your resume to proceed.")

# Generate Cover Letter
if generate_cover_letter_button:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        with st.spinner("Generating cover letter..."):
            cover_letter = get_gemini_response(input_text, pdf_content, input_prompt_cover_letter)
            st.subheader("Tailored Cover Letter")
            st.write(cover_letter)
    else:
        st.warning("Please upload your resume to proceed.")

# Generate Tailored Resume
if generate_resume_button:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        with st.spinner("Generating tailored resume..."):
            tailored_resume = get_gemini_response(input_text, pdf_content, input_prompt_resume)
            st.subheader("Tailored Resume")
            st.write(tailored_resume)
    else:
        st.warning("Please upload your resume to proceed.")

# Footer with credits and links
st.markdown("""
    <div class='footer'>
        Developed by  <strong>Muhammed Nifal C H</strong> |
        <a href='https://in.linkedin.com/in/muhammed-nifal-c-h' target='_blank'>LinkedIn</a> |
        <a href='https://github.com/Nifalch' target='_blank'>GitHub</a> |
        <a href='https://nifalch.github.io/portfolio-website/' target='_blank'>Portfolio</a>
    </div>
""", unsafe_allow_html=True)
