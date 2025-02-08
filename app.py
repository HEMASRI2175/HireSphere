import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import base64
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Function to interact with Gemini AI
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input)
    return response.text

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        text += str(page.extract_text())
    return text

input_prompt ="""

### As a skilled Application Tracking System (ATS) with advanced knowledge in technology and data science, your role is to meticulously evaluate a candidate's resume based on the provided job description. 

### Your evaluation will involve analyzing the resume for relevant skills, experiences, and qualifications that align with the job requirements. Look for key buzzwords and specific criteria outlined in the job description to determine the candidate's suitability for the position.

### Provide a structured and formatted assessment that follows these guidelines:

### **Evaluation Output:**
#### 1. Percentage Match  
- provide it in Bold the percentage match (e.g., 70%) and remove ** this symbols , give it in big and bold font
- Provide **two justification points** explaining why this percentage was assigned.  

#### **2. Missing Keywords**  
- **List of missing keywords first (bullet points)**  
- Then, provide a **detailed explanation** of how including these keywords will improve alignment with the job description.  

#### **3. Resume Enhancement Tips**  
- Offer **specific and actionable tips** to improve the resume’s alignment with the job description.  
- **Use concise bullet points** for readability.  

#### **4. Job Role Fit**  
- **Assess whether the candidate is a strong fit** for the exact job title or better suited for an alternative role.  
- Provide insights on **alternative job roles** that match their skill set.  

#### **5. Resume-Enhancing Words & Phrases**  
- Give this is tabular format
- Identify **weak or vague wording** and suggest **strong, action-oriented replacements**.  
- Provide a **list of impactful action verbs** and professional terminology.  

#### **6. Relevant Certifications**  
- Suggest industry-recognized **certifications** that align with the job requirements.  
- Recommend online courses or training programs (e.g., **Coursera, Udemy, LinkedIn Learning**).  

#### **7. Recommended Resources**   
- **Top YouTube videos** for learning key job-related skills  
- **Industry blogs/articles** providing career insights
- **Expert guides for resume optimization & interview prep**  



resume={text}  
jd={jd}  

"""


st.set_page_config(page_title="HireSphere - Smart ATS", page_icon="💼", layout="wide")

with st.sidebar:
    # Sidebar Navigation with Styling
    st.markdown("""
        <style>
            .sidebar-links {
                color: white !important;
                text-align: left;
                padding: 10px 20px;
                font-size: 24px;
                font-weight: bold;
                display: flex;
                align-items: center;
                text-decoration: none !important;
                border-radius: 8px;
                transition: background 0.3s ease;
            }
            .sidebar-links img {
                margin-right: 10px;
                width: 24px;  /* Adjust icon size */
                height: 24px;
                filter: brightness(1) invert(1); /* Ensures visibility on dark background */
            }
            .sidebar-links:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            .sidebar-container {
                padding: 15px;
                margin: 10px;
                border-radius: 10px;
            }
        </style>
        
        <div class="sidebar-container">
            <a href="#home" class="sidebar-links">🏠 Home</a>
            <a href="#ats-score" class="sidebar-links">📊 ATS Score</a>
            <a href="#about" class="sidebar-links">ℹ️ About</a>
            <a href="#contact" class="sidebar-links">📞 Contact Us</a>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")  # Separator for better UI

    # "How It Works" Section
    st.subheader("📌 How It Works")
    st.markdown(f"""
    <div style="text-align: left; font-size: 18px;">
        1️⃣ <b>Paste your Job Description</b><br>
        2️⃣ <b>Upload your Resume (PDF)</b><br>
        3️⃣ <b>Click 'Analyze Resume'</b><br>
        4️⃣ <b>Get ATS Match Score & Improvement Tips!</b>
    </div>
    """, unsafe_allow_html=True)


# Adding an anchor div for navigation
st.markdown('<div id="home" class="anchor"></div>', unsafe_allow_html=True)

# Custom CSS for Responsive Design
st.markdown("""
    <style>
        /* Global Styling */
        html, body {
            font-family: 'Arial', sans-serif;
        }

        /* Center Headings */
        h1, h3, p {
            text-align: center;
        }

        /* Adjust padding for different screen sizes */
        @media screen and (max-width: 768px) {
            .stTextArea, .stFileUploader {
                width: 100% !important;
            }
            .stButton {
                display: flex;
                justify-content: center;
                width: 100%;
            }
        }

        /* Sidebar adjustments */
[data-testid="stSidebar"] {
    background-color: #00000;
    padding: 20px;
    border-right: 2px solid #8E4256; /* Adds a subtle border for definition */
}

/* Responsive Design for Different Screens */
@media (max-width: 1024px) {
    [data-testid="stSidebar"] {
        padding: 15px;
    }
}

@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        padding: 10px;
        border-right: none; /* Remove border for smaller screens */
        text-align: center; /* Center-align content for a cleaner look */
    }
}

@media (max-width: 480px) {
    [data-testid="stSidebar"] {
        padding: 8px;
        font-size: 14px; /* Adjust font size for readability */
    }
}


        /* Footer Styling */
        .footer {
            position: relative;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #6A3F4A;
        }
    </style>
""", unsafe_allow_html=True)
image_path = r"C:\Users\HEMU\Desktop\ats-mlapp\download (6).png"
image = r"C:\Users\HEMU\Desktop\ats-mlapp\image.png"
# Function to encode image in Base64
def get_base64_image(image):
    with open(image, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Convert image to Base64
image_base64 = get_base64_image(image)

st.markdown(
    f"""
    <div style="display: flex; justify-content: center; ">
        <img src="data:image/png;base64,{image_base64}" width="350">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <h3 style="text-align: center; color: #ff5757;"> Match. Optimize. Succeed.</h3>
    <p style="text-align: center; color: #ff5757;">
        Your AI-powered ATS for Resume Optimization & Job Matching!
    </p>
""", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""<hr style="border: 1px solid #8E4256;">""", unsafe_allow_html=True)
# Section Heading
st.markdown('<div id="ats-score" class="anchor"></div>', unsafe_allow_html=True)
st.header("📊 ATS Score")

# Introduction and How It Works
st.markdown(
    """
    <div style="background-color: #262730; padding: 20px; border-radius: 10px; text-align: left; color: white;">
        <p>Welcome to <b>HireSphere's Smart ATS Resume Analyzer!</b> Our AI-powered system evaluates your resume against a job description to provide actionable insights, ensuring higher <b>ATS (Applicant Tracking System) compatibility</b> and increasing your chances of landing interviews.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# What Users Will Get
st.markdown(
    """
    <div style="background-color: #170c10; padding: 20px; border-radius: 10px; text-align: left; color: white; margin-top: 20px;">
        <h3 style="text-align: center;">📌 What You’ll Get in the Analysis?</h3>
        <ul style="font-size: 18px;">
            <li>✅ <b>ATS Score (%)</b> – Your resume’s compatibility with the job description.</li>
            <li>✅ <b>Missing Keywords</b> – Important skills and industry terms your resume lacks.</li>
            <li>✅ <b>Resume Enhancement Tips</b> – Actionable recommendations to optimize content & formatting.</li>
            <li>✅ <b>Job Role Fit Analysis</b> – Determines if your resume aligns with the applied job.</li>
            <li>✅ <b>Resume-Enhancing Words & Phrases</b> – Suggestions for impactful wording.</li>
            <li>✅ <b>Relevant Certifications</b> – Recommended industry-recognized certifications to boost credibility.</li>
            <li>✅ <b>Career Resources</b> – Expert articles, YouTube tutorials, and interview prep guides.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# Why Use This Tool?

# ATS Analysis Form Section
col1, col2 = st.columns([2, 3])  # Adjusted ratio for better responsiveness

with col1:
    jd = st.text_area("📌 Paste Your Job Description", placeholder="Enter job description here...", height=200)

with col2:
    uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"], help="Only PDF files are supported.")

# Center the Button for all screen sizes
if st.button("🔍 Analyze Resume"):
    if uploaded_file is not None:
        with st.spinner("⏳ Analyzing your resume... Please wait!"):
            text = input_pdf_text(uploaded_file)
            response = get_gemini_response(input_prompt.format(text=text, jd=jd))

        # Display Output
        st.markdown("### 🎯 ATS Evaluation Results", unsafe_allow_html=True)

        st.markdown(f"""
            <div style="text-align: left; font-size: 18px;">
                {response}
        """, unsafe_allow_html=True)

        # Download Report Button
        st.download_button(
            label="📥 Download Report",
            data=response.encode("utf-8"),
            file_name="ATS_Resume_Evaluation.txt",
            mime="text/plain"
        )
    else:
        st.warning("⚠️ Please upload a PDF resume before analyzing!")

st.markdown("""<hr style="border: 1px solid #8E4256;">""", unsafe_allow_html=True)


st.markdown('<div id="about" class="anchor"></div>', unsafe_allow_html=True)
import streamlit as st

# Section Header
st.header("About")
st.markdown(
    """
    <div style="background-color: #8E4256; padding: 20px; border-radius: 10px; text-align: left; color: white; margin-top: 20px;">
        <h3 style="text-align: center;">🎯 Why Use This Tool?</h3>
        <ul style="font-size: 18px;">
            <li><b>Maximize Resume Visibility</b> – Get past ATS filters used by recruiters.</li>
            <li><b>Improve Job Match Score</b> – Tailor your resume for better alignment.</li>
            <li><b>Optimize for AI Screening</b> – Ensure your application is noticed by hiring managers.</li>
            <li><b>Fast & Easy</b> – Instant analysis with a detailed improvement report.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<br><br>", unsafe_allow_html=True)
# Creating a responsive layout for three cards
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Encode the three images
image1_base64 = get_base64_image("C:/Users/HEMU/Desktop/ats-mlapp/1.png")
image2_base64 = get_base64_image("C:/Users/HEMU/Desktop/ats-mlapp/2.png")
image3_base64 = get_base64_image("C:/Users/HEMU/Desktop/ats-mlapp/3.png")

# Creating a responsive layout for three cards
st.markdown(
    """
    <style>
        @media screen and (max-width: 768px) {
            .responsive-card {
                margin-bottom: 25px !important;  /* Add space between stacked cards */
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Creating a responsive layout for three cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="responsive-card" style="text-align: center; padding: 20px; border-radius: 10px; 
                     background-color: #262730; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <img src="data:image/png;base64,{image1_base64}" width="300">
            <h5 style="padding-top: 20px; padding-bottom: 10px;">AI-Powered Resume Analysis</h5>
            <p>Leverage advanced AI algorithms to evaluate resumes against job descriptions, ensuring higher ATS compatibility and increasing interview chances.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="responsive-card" style="text-align: center; padding: 20px; border-radius: 10px; 
                     background-color: #262730; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <img src="data:image/png;base64,{image2_base64}" width="300">
            <h5 style="padding-top: 27px; padding-bottom: 10px;">Personalized Career Insights</h5>
            <p>Receive detailed feedback on missing skills, optimization tips, and job role fit analysis to align your resume with industry standards and employer expectations.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        f"""
        <div class="responsive-card" style="text-align: center; padding: 20px; border-radius: 10px; 
                     background-color: #262730; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <img src="data:image/png;base64,{image3_base64}" width="300">
            <h5 style="padding-top: 20px; padding-bottom: 10px;">ATS Compatibility Boost</h5>
            <p>Optimize your resume with industry-specific keywords, strong action verbs, and structured formatting to pass ATS filters. Ensure clear, scannable content by avoiding excessive formatting </p>
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown("""<hr style="border: 1px solid #8E4256;">""", unsafe_allow_html=True)
# Contact Section
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

st.markdown('<a name="contact-us"></a>', unsafe_allow_html=True)

def send_email(name, sender_email, message):
    try:
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email_address = "chettimchettyhemasri@gmail.com"  
        sender_email_password = "xmvb syyz audm kuzh"  

        # Recipient email
        recipient_email = "chettimchettyhemasri@gmail.com"

        # Email content
        subject = f"New Contact Form Submission from {name}"
        body = f"""
        You have received a new message from the contact form:
        
        Name: {name}
        Email: {sender_email}
        Message:
        {message}
        """

        # Create email
        msg = MIMEMultipart()
        msg["From"] = sender_email_address
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email_address, sender_email_password)
        server.sendmail(sender_email_address, recipient_email, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# Contact Form
with st.container():
    st.header("Contact Us")
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")

    if st.button("Send Message"):
        if name and email and message:
            # Call the send_email function
            if send_email(name, email, message):
                st.success("Your message has been sent successfully!")
            else:
                st.error("Failed to send your message. Please try again later.")
        else:
            st.warning("Please fill out all fields before sending.")

    st.markdown('</div>', unsafe_allow_html=True)



# Footer
st.markdown("""
    <hr>
    <div class='footer'>
        © 2024 HireSphere. All Rights Reserved. 🚀
    </div>
""", unsafe_allow_html=True)
