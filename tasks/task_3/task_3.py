# pdf_processing.py

# Necessary imports
import streamlit as st #웹 애플리케이션을 만듬
from langchain_community.document_loaders import PyPDFLoader #pdf 파일을 로드하고 처리하는데 사용
import os #파일을 경로와 임시파일 관리 위해 사용
import tempfile #
import uuid #고유한 파일 이름 생성하는데 사용

class DocumentProcessor:#pdf 문서 처리 기능 캡슐화
    """
    This class encapsulates the functionality for processing uploaded PDF documents using Streamlit
    and Langchain's PyPDFLoader. It provides a method to render a file uploader widget, process the
    uploaded PDF files, extract their pages, and display the total number of pages extracted.
    """
    def __init__(self):
        self.pages = []  # List to keep track of pages from all documents
    
    def ingest_documents(self):
        """
        Renders a file uploader in a Streamlit app, processes uploaded PDF files,
        extracts their pages, and updates the self.pages list with the total number of pages.
        
        Given:
        - Handling of temporary files with unique names to avoid conflicts.
        
        Your Steps:
        1. Utilize the Streamlit file uploader widget to allow users to upload PDF files.
           Hint: Look into st.file_uploader() with the 'type' parameter set to 'pdf'.
        2. For each uploaded PDF file:
           a. Generate a unique identifier and append it to the original file name before saving it temporarily.
              This avoids name conflicts and maintains traceability of the file.
           b. Use Langchain's PyPDFLoader on the path of the temporary file to extract pages.
           c. Clean up by deleting the temporary file after processing.
        3. Keep track of the total number of pages extracted from all uploaded documents.
        
        Example for generating a unique file name with the original name preserved:
        ```
        unique_id = uuid.uuid4().hex
        temp_file_name = f"{original_name}_{unique_id}{file_extension}"
        ```
        """
        
        # Step 1: Render a file uploader widget. Replace 'None' with the Streamlit file uploader code.
        uploaded_files = st.file_uploader(
            #####################################
            # Allow only type `pdf`
            # Allow multiple PDFs for ingestion
            #####################################
            "Upload PDF File",
            type = ['pdf'],#오직 pdf 파일만 
            accept_multiple_files=True#여러개의 파일을 한번에 업로드 하게 도와줌
        )
        
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:#반복문
                # Generate a unique identifier to append to the file's original name
                unique_id = uuid.uuid4().hex
                original_name, file_extension = os.path.splitext(uploaded_file.name)
                temp_file_name = f"{original_name}_{unique_id}{file_extension}"
                temp_file_path = os.path.join(tempfile.gettempdir(), temp_file_name)
                                
                # Write the uploaded PDF to a temporary file
                with open(temp_file_path, 'wb') as f:#업로드된 파일을 임시파일로 저장
                    f.write(uploaded_file.getvalue())

                # Step 2: Process the temporary file
                #####################################
                # Use PyPDFLoader here to load the PDF and extract pages.
                # https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf#using-pypdf
                # You will need to figure out how to use PyPDFLoader to process the temporary file.
                
                try:
                    # Initialize PyPDFLoader with the path to the temporary file
                    pdf_loader = PyPDFLoader(temp_file_path)

                    # Load the pages from the PDF
                    extracted_pages = pdf_loader.load()

                # Step 3: Then, Add the extracted pages to the 'pages' list.
                #####################################
                    self.pages.extend(extracted_pages)
                finally:
                    # Clean up by deleting the temporary file.
                    os.unlink(temp_file_path)
            
            # Display the total number of pages processed.
            st.write(f"Total pages processed: {len(self.pages)}")
        
if __name__ == "__main__":
    processor = DocumentProcessor()
    processor.ingest_documents()
