import streamlit as st
import requests
import base64
import json
from PIL import Image
import fitz 

# Streamlit UI Title
st.title("📄 Validação de Documentos")

st.write("""
### Faça o upload dos documentos necessários:
1. **Documento com Foto (CNH Nova Versão)** (PNG, JPG, JPEG)
2. **Foto de Rosto** (PNG, JPG, JPEG)
3. **Comprovante de Residência** (PDF)
""")

# File Uploaders
document_file = st.file_uploader("📷 Enviar Documento com Foto (CNH Nova Versão)", type=["png", "jpg", "jpeg"])
validation_file = st.file_uploader("📷 Enviar Foto de Rosto", type=["png", "jpg", "jpeg"])
residence_file = st.file_uploader("📄 Enviar Comprovante de Residência (PDF)", type=["pdf"])

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
    with st.spinner("Processando documentos..."):
        
        # Convert files to Base64
        document_base64 = convert_image_to_base64(document_file)
        validation_base64 = convert_image_to_base64(validation_file)
        residence_base64 = convert_pdf_to_base64(residence_file)

        if not residence_base64:
            st.error("Erro ao converter o PDF para imagem. Por favor, envie um PDF válido.")
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
                st.success("✅ Documentos validados com sucesso!")
                
                # Display extracted information
                st.write("### Informações Extraídas:")
                st.write(f"**Nome:** {response_data['name']}")
                st.write(f"**CPF:** {response_data['cpf']}")
                st.write(f"**Validação da Foto:** {'✅ Sim' if response_data['photo_validation'] else '❌ Não'}")
                st.write(f"**Porcentagem de Similaridade da Foto:** {response_data['photo_similarity']:.2f}%")
                st.write(f"**Validação do Nome da CNH com Comprovante de Residência:** {'✅ Sim' if response_data['name_validation'] else '❌ Não'}")
                st.write(f"**Endereço:** {response_data['address']}")
                
            else:
                st.error(f"🚨 Erro {response.status_code}: {response.text}")