import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

def extract_images_from_page(page, doc):
    # Extract images from the page
    images = []
    for img in page.get_images(full=True):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        images.append(io.BytesIO(image_bytes))
    return images

def format_text_blocks(blocks):
    formatted_text = ""
    for block in blocks:
        if block['type'] == 0:  # Text block
            for line in block['lines']:
                line_text = ""
                for span in line['spans']:
                    # Simple heuristic for indentation
                    if span['size'] > 14:  # Potential headings
                        line_text += f"## {span['text']} "
                    else:
                        line_text += span['text'] + " "
                formatted_text += line_text.strip() + "\n"
            formatted_text += "\n"  # Add extra space between text blocks
    return formatted_text

def display_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    num_pages = doc.page_count

    for page_number in range(num_pages):
        page = doc.load_page(page_number)
        
        # Extract and format text
        blocks = page.get_text("dict")['blocks']
        formatted_text = format_text_blocks(blocks)
        st.markdown(f"### Page {page_number + 1}")
        st.markdown(formatted_text)

        # Extract and display images
        images = extract_images_from_page(page, doc)
        if images:
            st.write("Images (including tables and charts) on this page:")
        for img_index, img in enumerate(images):
            image = Image.open(img)
            st.image(image, caption=f"Image {img_index + 1} on Page {page_number + 1}", use_column_width=True)

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
