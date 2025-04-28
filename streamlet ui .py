import streamlit as st
import base64

# Function to read the uploaded PDF file and encode it in base64
def get_pdf_base64(file):
    pdf_bytes = file.read()
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
    return pdf_base64

# Streamlit UI
st.title("PDF Processing Tool")

# File uploader for the original PDF
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    # Convert the uploaded file to base64 for embedding
    original_pdf_base64 = get_pdf_base64(uploaded_file)
    
    # Define a placeholder for the processed PDF (you can apply your processing here)
    processed_pdf_base64 = original_pdf_base64  # You can replace this with a processed PDF

    # Split the layout into two parts: one for original PDF and one for processed PDF
    col1, col2 = st.columns(2)

    with col1:
        st.header("Original PDF")
        # Embed the original PDF in an iframe
        st.markdown(f'<iframe src="data:application/pdf;base64,{original_pdf_base64}" width="700" height="500"></iframe>', unsafe_allow_html=True)

    with col2:
        st.header("Processed PDF")
        # Embed the processed PDF in an iframe
        st.markdown(f'<iframe src="data:application/pdf;base64,{processed_pdf_base64}" width="700" height="500"></iframe>', unsafe_allow_html=True)
