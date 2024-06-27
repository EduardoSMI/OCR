import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract as pt
from PIL import Image
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO

st.title('OCR em PDF')


# Função para realizar OCR em uma imagem e retornar o texto
def ocr_image(img):
    text = pt.image_to_string(img)
    return text


# Função para converter texto em um arquivo PDF e baixar
def download_pdf(pdf_writer, filename='output.pdf'):
    buffer = BytesIO()
    pdf_writer.write(buffer)
    buffer.seek(0)

    st.download_button(
        label="Baixar PDF com OCR",
        data=buffer,
        file_name=filename,
        mime="application/pdf"
    )


uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=['pdf'])

if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()

    if st.button('Processar PDF'):
        # Converter PDF em imagens
        images = convert_from_bytes(pdf_bytes)

        # Inicializar PDF writer para salvar texto
        output_pdf = PdfWriter()

        # Processar cada página convertida em imagem
        with st.spinner('Processando...'):
            for i, image in enumerate(images):
                #st.image(image, caption=f'Página {i + 1}')  # Exibir a imagem

                # Realizar OCR na imagem
                text = ocr_image(image)

                # Adicionar texto ao PDF de saída
                img_pdf = pt.image_to_pdf_or_hocr(image, extension="pdf")
                input_pdf = PdfReader(BytesIO(img_pdf))

                # Adicionar página ao PDF de saída
                output_pdf.add_page(input_pdf.pages[0])

        # Gerar e disponibilizar link para download do PDF com OCR
        download_pdf(output_pdf)
