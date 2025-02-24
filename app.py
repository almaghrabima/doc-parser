import streamlit as st
import os
from pathlib import Path
from docling.backend.docling_parse_backend import DoclingParseDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    EasyOcrOptions,
    OcrMacOptions,
    PdfPipelineOptions,
    RapidOcrOptions,
    TesseractCliOcrOptions,
    TesseractOcrOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption

def main():
    st.title("File Selection App")
    
    # Initialize session state for storing the concatenated path
    if 'full_file_path' not in st.session_state:
        st.session_state.full_file_path = None
    
    # Add description
    st.write("Select a file from your computer to view its path information")
    
    # File uploader with type filtering
    allowed_types = ["pdf", "doc", "docx", "ppt", "pptx", "jpg", "jpeg"]
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=allowed_types,
        help="Supported files: PDF, Word, PowerPoint, and JPEG"
    )
    
    # Display file details if a file is uploaded
    if uploaded_file is not None:
        # Save the uploaded file to the /app directory
        save_path = os.path.join('/app', uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.full_file_path = save_path
        
        file_details = {
            "Filename": uploaded_file.name,
            "Full Path": save_path,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type,
            "Concatenated Path Variable": st.session_state.full_file_path
        }
        
        st.write("### File Details:")
        for key, value in file_details.items():
            st.write(f"**{key}:** {value}")
        
        st.write("### Using the Concatenated Path")
        st.code(f'''
# You can access the full file path anywhere in your app using:
full_file_path = st.session_state.full_file_path

if st.session_state.full_file_path:
    print(f'Working with file: {st.session_state.full_file_path}')
        ''')
        
        if st.button("Print Path to Console"):
            st.write(f"Path has been printed to console: {st.session_state.full_file_path}")
            print(f"Full file path: {st.session_state.full_file_path}")
        
        st.info("Note: The full path shown is where the file is saved in the container. "
                "The original file path on your local machine is not accessible due to browser security restrictions.")
        
    if st.session_state.full_file_path:
        input_doc = st.session_state.full_file_path

        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True

        ocr_options = TesseractCliOcrOptions(force_full_page_ocr=True)
        pipeline_options.ocr_options = ocr_options

        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                )
            }
        )

        doc = converter.convert(input_doc).document
        md = doc.export_to_markdown()
        print(md)

if __name__ == "__main__":
    main()