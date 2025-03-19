import os
import json
import time
import markdown
import requests
from pathlib import Path
from utils import read_file_paths, validate_json_save_path, load_json_file

CATEGORY_MAP = {
    "text": "paragraph",
    "heading": "heading1",
    "table": "table"
}

class LlamaParseInference:
    def __init__(self, api_key, post_url, get_url):
        """Initialize the LlamaParseInference class"""
        self.api_key = api_key
        self.post_url = post_url
        self.get_url = get_url

        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def post_process(self, data):
        """Post-process the results"""
        processed_dict = {}
        for input_key, output_data in data.items():
            processed_dict[input_key] = {"elements": []}
            id_counter = 0

            for elem in output_data.get("pages", []):
                for item in elem.get("items", []):
                    category = CATEGORY_MAP.get(item["type"], "paragraph")

                    transcription = markdown.markdown(
                        item.get("md", ""),
                        extensions=["markdown.extensions.tables"]
                    ) if category == "table" else item.get("value", "")

                    data_dict = {
                        "id": id_counter,
                        "category": category,
                        "content": {
                            "text": transcription if category != "table" else "",
                            "html": transcription if category == "table" else "",
                            "markdown": ""
                        }
                    }
                    processed_dict[input_key]["elements"].append(data_dict)
                    id_counter += 1

        return processed_dict

    def infer(self, file_path, save_path):
        """Infer the layout of the documents in the given file path"""
        
        paths = read_file_paths(file_path)
        
        
        filepath = paths 

        result_dict = {}
        # for filepath in paths:
        # print(f"Processing: {filepath}")

        try:
            with open(filepath, "rb") as file_data:
                file_data = {"file": ("dummy.pdf", file_data, "")}
                data = {
                    "invalidate_cache": True,
                    "premium_mode": True,
                    "disable_ocr": False
                }
                response = requests.post(self.post_url, headers=self.headers, files=file_data, data=data
                )
            result_data = response.json()
            status = result_data["status"]
            id_ = result_data["id"]

            while status == "PENDING":
                get_url = f"{self.get_url}/{id_}"
                response = requests.get(get_url, headers=self.headers)

                response_json = response.json()
                status = response_json["status"]
                if status == "SUCCESS":
                    get_url = f"{self.get_url}/{id_}/result/json"
                    response = requests.get(get_url, headers=self.headers)
                    break

                time.sleep(1)

            filename = filepath.name
            result_dict[filename] = response.json()

        except Exception as e:
            print(f"Error processing {filepath}: {e}")


        # Post-process and save
        processed_data = self.post_process(result_dict)
        # print(processed_data)
        if processed_data:
            
            return processed_data 
        else:
            return None
