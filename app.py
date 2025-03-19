import requests
import os
import json
from dotenv import load_dotenv
import streamlit as st
from infer_llamaparse import LlamaParseInference
from pathlib import Path
import json
load_dotenv()
from model import get_llm_response

POST_URL = "https://api.cloud.llamaindex.ai/api/parsing/upload"
GET_URL = "https://api.cloud.llamaindex.ai/api/parsing/job"

# Check environment
try:
    st.secrets
    # Running on Streamlit Cloud
    st.write("Running on Streamlit Cloud")
    API_KEY = st.secrets["LLAMAPARSE_API_KEY"]
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    # Running locally
    st.write("Running on Local Machine")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    API_KEY = os.getenv("LLAMAPARSE_API_KEY")



# Streamlit UI
st.title("📄 PDF Table Extractor with LlamaParse")

# Upload PDF
uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    file_path = Path("uploads") / uploaded_file.name
    
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    st.success(f"File uploaded successfully: {uploaded_file.name}")

    # Output JSON path
    output_path = "output.json"

    # Initialize and run the LlamaParse inference
    st.info("Running PDF extraction...")

    llama_parser = LlamaParseInference(
        api_key=API_KEY,
        post_url=POST_URL,
        get_url=GET_URL
    )

    try:
        # print(file_path)
        processed_data = llama_parser.infer(file_path, output_path)
        st.success("Extraction completed successfully!")


        if processed_data:
            response = get_llm_response(processed_data,OPENAI_API_KEY)
            import time
            result_folder = Path('Result')
            if not os.path.exists(result_folder):
                os.makedirs(result_folder,exist_ok=True)
            
            file_path = os.path.join(result_folder,f"OuputFile{time.time()}.json")

            with open(file_path,'w') as f:
                json.dump(response,f)

            st.download_button(
                label="⬇️ Download Extracted JSON",
                data=json.dumps(response, indent=4),  # Convert dict to string for download
                file_name="extracted_data.json",
                mime="application/json"
            )

            try:
                st.json(response)
            except:
                st.text_area("Extracted JSON", response, height=400)

            # Download button



        else:
            st.error("No output generated!")

    except Exception as e:
        st.error(f"Error during extraction: {e}")

