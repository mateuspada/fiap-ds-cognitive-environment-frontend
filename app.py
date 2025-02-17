import streamlit as st
import requests
import base64
import json
from PIL import Image
from pdf2image import convert_from_bytes

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
    """Convert PDF file to Base64 string after converting to image."""
    images = convert_from_bytes(pdf_file.read())  # Convert PDF to images
    if images:
        img_bytes = images[0].tobytes("jpeg", "RGB")  # Convert first page to JPEG
        return base64.b64encode(img_bytes).decode("utf-8")
    return None

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
                st.write("### 🆔 Extracted Information:")
                st.write(f"**Name:** {response_data['body']['name']}")
                st.write(f"**CPF:** {response_data['body']['cpf']}")
                st.write(f"**Photo Validation:** {'✅ Yes' if response_data['body']['photo_validation'] else '❌ No'}")
                st.write(f"**Photo Similarity Score:** {response_data['body']['photo_similarity']:.4f}")
                st.write(f"**Name Validation:** {'✅ Yes' if response_data['body']['name_validation'] else '❌ No'}")
                st.write(f"**Extracted Address:** {response_data['body']['address']}")
                
            else:
                st.error(f"🚨 Error {response.status_code}: {response.text}")