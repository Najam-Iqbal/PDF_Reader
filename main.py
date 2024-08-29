import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

def extract_table_images(page):
    # Extract tables as images
    images = []
    for img in page.get_images(full=True):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        images.append(io.BytesIO(image_bytes))
    return images

def display_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    num_pages = doc.page_count

    for page_number in range(num_pages):
        page = doc.load_page(page_number)
        
        # Extract and display text
        blocks = page.get_text("dict")['blocks']
        formatted_text = ""
        for block in blocks:
            if block['type'] == 0:  # Text block
                for line in block['lines']:
                    for span in line['spans']:
                        if span['size'] > 14:  # Simple heuristic for headings
                            formatted_text += f"## {span['text']}\n\n"
                        else:
                            formatted_text += f"{span['text']} "
                    formatted_text += "\n\n"
        st.markdown(f"### Page {page_number + 1}")
        st.markdown(formatted_text)

        # Extract and display images
        image_list = page.get_images(full=True)
        if image_list:
            st.write("Images on this page:")
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption=f"Image {img_index + 1} on Page {page_number + 1}", use_column_width=True)

        # Extract and display tables as images
        table_images = extract_table_images(page)
        if table_images:
            st.write("Tables and charts on this page:")
        for img_index, img in enumerate(table_images):
            image = Image.open(img)
            st.image(image, caption=f"Table/Chart {img_index + 1} on Page {page_number + 1}", use_column_width=True)

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
