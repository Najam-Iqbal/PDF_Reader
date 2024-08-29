import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

# Function to extract and display text and images
def display_pdf_content(pdf_path, zoom=2):
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Extract and display text
        text = page.get_text("text")
        if text.strip():
            st.text_area(f"Text from Page {page_num + 1}", text, height=300, key=f"text_area_{page_num}")

        # Extract and display images
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            img = Image.open(io.BytesIO(image_bytes))
            st.image(img, caption=f'Image from Page {page_num + 1} - Image {img_index + 1}', use_column_width=True)
        
    doc.close()

# Streamlit app
def main():
    st.title("Enhanced PDF Reader")

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        # Save the uploaded file
        pdf_path = "temp.pdf"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())
        
        st.success("PDF uploaded successfully!")
        st.write("Opening PDF...")
        
        # Display the PDF content (text and images)
        display_pdf_content(pdf_path, zoom=2)  # Adjust zoom factor as needed

if __name__ == "__main__":
    main()
