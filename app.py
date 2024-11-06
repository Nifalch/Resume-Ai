import streamlit as st
import base64
import os
import io
import fitz  # PyMuPDF
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Helper function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")  # Extract text from each page
    return text

# AI model function
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

# Streamlit App Config with Custom Favicon
st.set_page_config(
    page_title="Resume AI",
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
        width: 150px;
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
        height: 50px;
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

    .button-column {
        display: flex;
        justify-content: space-around;
        align-items: stretch;
    }
    
    </style>
""", unsafe_allow_html=True)

# Logo Section - Centered Logo
logo_path = "aire.png"
if os.path.exists(logo_path):
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image(logo_path, width=250)
    st.markdown("</div>", unsafe_allow_html=True)

# Job Description Input Section
st.subheader("Job Description")
input_text = st.text_area("Enter the Job Description", placeholder="Paste the job description here...", key="input")

# Resume Upload Section
st.markdown("<div class='upload-area'>Upload your resume (PDF only)</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["pdf"])

# Action Buttons
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
with col1:
    analyze_button = st.button("Analyze Resume")
with col2:
    match_button = st.button("ATS Score")
with col3:
    generate_cover_letter_button = st.button("Generate Cover Letter")
with col4:
    generate_resume_button = st.button("Generate Tailored Resume")

# Prompts
input_prompt1 = "As an experienced HR Manager, review the provided resume against the job description. Assess how well the candidate’s profile aligns with the role, noting key strengths and areas for improvement."
input_prompt3 = "As a skilled ATS system, evaluate the resume based on the job description. Provide a match percentage, list missing keywords, and share an overall assessment."
input_prompt_cover_letter = "Based on the job description and my uploaded resume, create a professional cover letter that highlights my relevant skills and experiences."
input_prompt_resume = "Using the provided job description and resume, create a tailored resume highlighting the relevant skills, experience, and qualifications that match the job description."

# Analysis & Response
if analyze_button:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        with st.spinner("Analyzing resume..."):
            response = get_gemini_response(input_text, pdf_text, input_prompt1)
            st.subheader("Resume Analysis")
            st.write(response)
    else:
        st.warning("Please upload your resume to proceed.")

elif match_button:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        with st.spinner("Calculating match percentage..."):
            response = get_gemini_response(input_text, pdf_text, input_prompt3)
            st.subheader("Match Percentage & Recommendations")
            st.write(response)
    else:
        st.warning("Please upload your resume to proceed.")

if generate_cover_letter_button:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        with st.spinner("Generating cover letter..."):
            cover_letter = get_gemini_response(input_text, pdf_text, input_prompt_cover_letter)
            st.subheader("Tailored Cover Letter")
            st.write(cover_letter)
    else:
        st.warning("Please upload your resume to proceed.")

if generate_resume_button:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        with st.spinner("Generating tailored resume..."):
            tailored_resume = get_gemini_response(input_text, pdf_text, input_prompt_resume)
            st.subheader("Tailored Resume")
            st.write(tailored_resume)
    else:
        st.warning("Please upload your resume to proceed.")

# Footer with credits and links
st.markdown("""
    <div class='footer'>
        Developed by <strong>Muhammed Nifal C H</strong> |
        <a href='https://in.linkedin.com/in/muhammed-nifal-c-h' target='_blank'>LinkedIn</a> |
        <a href='https://github.com/Nifalch' target='_blank'>GitHub</a> |
        <a href='https://nifalch.github.io/portfolio-website/' target='_blank'>Portfolio</a>
    </div>
""", unsafe_allow_html=True)
