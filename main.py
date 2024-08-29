import streamlit as st
import pdfplumber
from PIL import Image
import io

def display_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        num_pages = len(pdf.pages)
        
        for page_number in range(num_pages):
            page = pdf.pages[page_number]
            
            # Render text and images
            text = page.extract_text()
            images = page.images

            # Display text
            st.write(f"### Page {page_number + 1}")
            st.write(text)

            # Display images
            for img in images:
                img_bbox = img['bbox']
                im = page.to_image()
                im = im.crop(img_bbox)
                img_byte_arr = io.BytesIO()
                im.save(img_byte_arr, format='PNG')
                st.image(img_byte_arr, caption=f"Image on Page {page_number + 1}", use_column_width=True)
                
        # Display total number of pages
        st.write(f"Total pages: {num_pages}")

def main():
    st.title('PDF Viewer')
    
    # Upload PDF
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file:
        # Save the uploaded file to a temporary location
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        
        # Display the PDF
        display_pdf("temp.pdf")

if __name__ == "__main__":
    main()
