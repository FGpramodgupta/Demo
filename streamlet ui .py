import streamlit as st
import PyPDF2
from io import BytesIO

# Function to load and display PDF
def load_pdf(file):
    reader = PyPDF2.PdfReader(file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text() + "\n"
    return pdf_text

# Streamlit UI
st.title("PDF Processing Tool")

# File uploader for PDF
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    # Split the layout into two parts
    col1, col2 = st.columns(2)
    
    with col1:
        # Display the original PDF content in the first column
        st.header("Original PDF")
        original_pdf = load_pdf(uploaded_file)
        st.text_area("Original PDF Content", original_pdf, height=400)
    
    with col2:
        # Dropdown for processing options
        st.header("Processed PDF")
        dropdown_option = st.selectbox("Choose Processing Option", ["Option 1", "Option 2"])
        
        # Placeholder for processed content
        if dropdown_option == "Option 1":
            # Here you can add your specific processing logic for Option 1
            st.text_area("Processed PDF Content", original_pdf[::-1], height=400)  # Example: reversing text
        elif dropdown_option == "Option 2":
            # Another processing logic
            st.text_area("Processed PDF Content", original_pdf.upper(), height=400)  # Example: converting to uppercase
