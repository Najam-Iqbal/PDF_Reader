import streamlit as st
import pdfplumber
from PIL import Image
import io

# Function to display PDF content (text and images)
def display_pdf_content(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            st.header(f"Page {page_num + 1}")

            # Extract and display text
            text = page.extract_text()
            if text:
                st.text_area(f"Text from Page {page_num + 1}", text, height=300, key=f"text_area_{page_num}")

            # Extract and display images
            for img_index, img in enumerate(page.images):
                # Extract the image's binary content
                img_obj = pdf.images[img_index]
                img_data = img_obj["stream"]
                img_pil = Image.open(io.BytesIO(img_data))
                st.image(img_pil, caption=f'Image from Page {page_num + 1} - Image {img_index + 1}', use_column_width=True)

# Streamlit app
def main():
    st.title("PDF Reader")

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        pdf_path = "temp.pdf"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success("PDF uploaded successfully!")
        st.write("Rendering PDF...")

        # Display the PDF content (text and images)
        display_pdf_content(pdf_path)

if __name__ == "__main__":
    main()
