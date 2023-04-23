import json
from pathlib import Path
from typing import Dict

import requests
import tiktoken
from rich import print_json

from summalarva.pdfextract import extract_pdf


class OpenAIClient:
    def __init__(self,
                 api_key,
                 host="https://api.openai.com",
                 model="text-davinci-003"
                 ):
        self.api_key = api_key
        self.host = host
        self.model = model
        self.encoder = tiktoken.encoding_for_model(model)

    def ask_gpt(self,
                ask: str,
                max_tokens=500,
                temperature=0.9,
                stop=None):
        if stop is None:
            stop = ["Human:", "AI:"]
        endpoint = f'{self.host}/v1/completions'
        data = {
            "model": self.model,
            "prompt": f"Human: {ask}\nAI:",
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop": stop
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(endpoint, json=data, headers=headers)
        if response.status_code != 200:
            print("The response is not 200")
            print(response.text)
            return None
        try:
            answer: str = response.json()['choices'][0]['text']
            answer = answer.strip()
            return answer
        except Exception as e:
            print("We have a bug here")
            print(e)
            pass
            # raise e

    def summary_page(self, page: str):
        summaries = []
        encode = self.encoder.encode(page)
        number_of_token = len(encode)
        chunks = []
        if number_of_token > 2048:
            chunks = [self.encoder.decode(encode[i:i + 2048]) for i in range(0, number_of_token, 2048)]
        else:
            chunks.append(page)
        print("The number of chunks is ", len(chunks))
        for chunk in chunks:
            if len(summaries) > 0:
                previous_sum = summaries[-1]
                new_summary = self.ask_gpt(f"The summarization of previous content is {previous_sum} \n\nNow "
                                           f"summarize the"
                                           f"content below:\n\n {chunk} \n\n")
                summaries.append(new_summary)
            else:
                new_summary = self.ask_gpt(f"Summarize the"
                                           f"below content: \n\n {chunk} \n\n")
                summaries.append(new_summary)
            # previous_summary = new_summary
        summary = "\n\n".join(summaries)
        return summary

    def summarize_document(self, document_path):
        document_path = Path(document_path).expanduser()
        pages = extract_pdf(document_path)
        summaries: Dict[int, str] = {}
        for page_num, page in enumerate(pages):
            summary = self.summary_page(page)
            summaries[page_num] = summary
        return summaries

    def get_info(self):
        endpoint = f'{self.host}/info'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        try:
            response = requests.get(endpoint, headers=headers)
            json_str = json.dumps(response.json(), indent=4)
            print_json(json_str)
        except Exception as e:
            print(e)

    def reset_ip(self):
        endpoint = f'{self.host}/resetip'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        try:
            response = requests.post(endpoint, headers=headers)
            json_str = json.dumps(response.json(), indent=4)
            print_json(json_str)
        except Exception as e:
            print(e)
