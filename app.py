import streamlit as st
import requests
import base64
import json
from PIL import Image
import fitz 

# Streamlit UI Title
st.title("📄 Cognitive Document Validation")

st.write("""
### Upload the required documents:
1. **Document with Photo** (PNG, JPG, JPEG)
2. **Validation Photo** (PNG, JPG, JPEG)
3. **Proof of Residence** (PDF)
""")

# File Uploaders
document_file = st.file_uploader("📷 Upload Document with Photo", type=["png", "jpg", "jpeg"])
validation_file = st.file_uploader("📷 Upload Validation Photo", type=["png", "jpg", "jpeg"])
residence_file = st.file_uploader("📄 Upload Proof of Residence (PDF)", type=["pdf"])

def convert_image_to_base64(image_file):
    """Convert an image file to Base64 string."""
    return base64.b64encode(image_file.read()).decode("utf-8")

def convert_pdf_to_base64(pdf_file):
    """Convert PDF to Base64 string after converting the first page to an image."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")  # Open PDF from bytes
    if len(doc) == 0:
        return None  # If PDF has no pages

    # Convert first page to an image
    pix = doc[0].get_pixmap()
    img_bytes = pix.tobytes("jpeg")  # Convert to JPEG bytes
    
    return base64.b64encode(img_bytes).decode("utf-8")

# Process and send to API only when all files are uploaded
if document_file and validation_file and residence_file:
    with st.spinner("Processing documents..."):
        
        # Convert files to Base64
        document_base64 = convert_image_to_base64(document_file)
        validation_base64 = convert_image_to_base64(validation_file)
        residence_base64 = convert_pdf_to_base64(residence_file)

        if not residence_base64:
            st.error("Error converting PDF to image. Please upload a valid PDF.")
        else:
            # Prepare the payload
            payload = {
                "document_image_base64": document_base64,
                "validation_image_base64": validation_base64,
                "residence_document_base64": residence_base64
            }

            # API Endpoint (Replace with actual API URL)
            API_ENDPOINT = st.secrets["API-ENDPOINT"]

            # Send Request to API
            response = requests.post(API_ENDPOINT, json=payload)

            # Process API response
            if response.status_code == 200:
                response_data = response.json()
                st.success("✅ Documents successfully validated!")
                
                # Display extracted information
                st.write("### Extracted Information:")
                st.write(f"**Name:** {response_data['name']}")
                st.write(f"**CPF:** {response_data['cpf']}")
                st.write(f"**Photo Validation:** {'✅ Yes' if response_data['photo_validation'] else '❌ No'}")
                st.write(f"**Photo Similarity Score:** {response_data['photo_similarity']:.4f}")
                st.write(f"**Name Validation:** {'✅ Yes' if response_data['name_validation'] else '❌ No'}")
                st.write(f"**Address:** {response_data['address']}")
                
            else:
                st.error(f"🚨 Error {response.status_code}: {response.text}")