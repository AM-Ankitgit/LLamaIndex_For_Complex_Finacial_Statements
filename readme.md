# 📄 **Financial Statement Extraction Using Llama Cloud and Streamlit**

### 🚀 **Overview**
This project is a **PDF financial statement extractor** using **Llama Cloud API** and **Streamlit**. It allows users to upload PDF files, extract financial tables, and display the results in JSON format. The app also provides the option to **download the extracted JSON**.

---

### ✅ **Features**
- 📄 Upload and extract financial statements from PDF.
- 🔥 Display extracted data in **JSON format**.
- ⬇️ Download the extracted JSON file.
- 🛠️ Error handling with validation and detailed logging.

---

### 🛠️ **Tech Stack**
- **Language:** Python
- **Framework:** Streamlit
- **API:** Llama Cloud (for document parsing)
- **Libraries:**  
  - `gpt model` → gpt-4o  
  - `requests` → To interact with the Llama Cloud API.
  - `json` → To format and display extracted data.
  - `os`, `pathlib` → For file management.
  - `argparse` → For command-line argument parsing.
  - `markdown` and `beautifulsoup4` → For HTML parsing.

---

### 🔧 **Installation**

1. **Clone the Repository**
```bash
git clone https://github.com/AM-Ankitgit/LLamaIndex_For_Complex_Finacial_Statements.git
cd LLamaIndex_For_Complex_Finacial_Statements

pip install -r requirements.txt

LLAMA Cloud_API_KEY=<your_api_key>  # https://cloud.llamaindex.ai/
LLAMA Cloud_POST_URL=https://api.cloud.llamaindex.ai/api/parsing/upload
LLAMA Cloud_GET_URL=https://api.cloud.llamaindex.ai/api/parsing/job


streamlit run app.py
http://localhost:8501




🔗 [Streamlit App]
##### https://llamaindexforcomplexfinacialstatements-ac3tb4gjr2ehuiqhw8zx4f.streamlit.app/