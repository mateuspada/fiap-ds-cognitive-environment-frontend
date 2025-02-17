# 🚀 FIAP - Cognitive Environment - Frontend

Este projeto faz parte do trabalho acadêmico na disciplina de **Cognitive Environments**, abordando **reconhecimento facial e extração de informações de documentos** usando **AWS Rekognition e Textract**.

## 📌 Objetivo do Projeto
O objetivo do projeto é criar uma interface web para validar documentos de identificação, extraindo **nome, CPF e endereço**, além de comparar a **foto do documento** com uma **foto de validação** para garantir a autenticidade do usuário.

## 🏷️ Estrutura do Projeto

O frontend foi desenvolvido utilizando **Streamlit** e se conecta ao backend hospedado no **AWS Lambda**.

1. **📃 Análise Exploratória (Jupyter Notebook)**
   - Testes usando **OpenCV (`cv2`), DLib e AWS Rekognition** para extração de face.
   - Extração de texto utilizando **AWS Textract**.
   - Comparação de Faces usando **AWS Rekognition**.

2. **🖙 Backend (AWS Lambda)**
   - Repositório: [`fiap-ds-cognitive-environment-backend`](https://github.com/mateuspada/fiap-ds-cognitive-environment-backend)
   - API Serverless em **AWS Lambda** usando **AWS Textract** e **AWS Rekognition**.

3. **🖥️ Frontend (Streamlit)**
   - Repositório: [`fiap-ds-cognitive-environment-frontend`](https://github.com/mateuspada/fiap-ds-cognitive-environment-frontend)
   - Interface web para o usuário fazer **upload das imagens** e visualizar os resultados.
   - Converte arquivos PDF em imagem automaticamente utilizando **PyMuPDF (fitz)**.

---

## 🖥️ Frontend: Streamlit Web Application

O frontend permite ao usuário **fazer upload** das imagens e visualizar os resultados do backend.

### 🛠️ Tecnologias
- **Streamlit** (Interface Web)
- **Requests** (para comunicação com a API)
- **Base64** (para conversão das imagens)
- **PyMuPDF (fitz)** (para converter PDFs em imagens)

### 📥 Entrada do Usuário
O usuário faz **upload** de três arquivos:
1. **Documento com Foto** (PNG, JPG, JPEG)
2. **Foto para Validação** (PNG, JPG, JPEG)
3. **Comprovante de Residência** (PDF)

### 📤 Comunicação com a API

O frontend envia os arquivos convertidos em Base64 para a API no seguinte formato:

```json
{
  "document_image_base64": "<imagem do documento>",
  "validation_image_base64": "<imagem para validação>",
  "residence_document_base64": "<comprovante de residência>"
}
```

A API então retorna um JSON com os resultados:

```json
{
  "statusCode": 200,
  "body": {
    "name": "<nome>",
    "cpf": "<cpf>",
    "photo_validation": true,
    "photo_similarity": 98.75,
    "name_validation": true,
    "address": "<address>"
  }
}
```

Caso ocorra um erro:

```json
{
  "statusCode": 400,
  "body": "Error in document photo: No face detected"
}
```

---

## ⚡ Como Rodar o Frontend Localmente

### 1️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Rode a aplicação Streamlit
```bash
streamlit run app.py
```

---

## 📌 Conclusão
Este projeto explora o uso de **Computer Vision e Reconhecimento Facial** para validação de documentos, integrando **AWS Rekognition** e **Textract** com uma interface web simples em **Streamlit**.