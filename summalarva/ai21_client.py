import json

import requests
from summalarva.pdfextract import extract_pdf
from pathlib import Path
from rich import print_json

ai21_endpoint = "https://api.ai21.com"
summarize_url = requests.compat.urljoin(ai21_endpoint, "/studio/v1/summarize")

api_key = None


def summary_page(page: str):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "source": page,
        "sourceType": "TEXT",
    }
    response = requests.post(url=summarize_url, json=data, headers=headers)
    if response.status_code != 200:
        print(response.json())
        return None
    try:
        answer: str = response.json()['summary']
        answer = answer.strip()
        return answer
    except Exception as e:
        print(response.json())
        raise e


def summarize_doc(doc_path: str | Path):
    if type(doc_path) == str:
        doc_path = Path(doc_path).expanduser()
    else:
        doc_path = doc_path.expanduser()
    pages = extract_pdf(doc_path)
    # split all page more than 50000 characters to smaller
    new_pages = []
    for page in pages:
        if len(page) > 50000:
            page_chunks = [page[i:i + 50000] for i in range(0, len(page), 50000)]
            new_pages.extend(page_chunks)
        else:
            new_pages.append(page)
    pages = new_pages

    summaries = []
    for page_num, page in enumerate(pages):
        print("Start processing page", page_num + 1)
        summary = summary_page(page)
        summaries.append(summary)
    return "\n\n".join(summaries)


def get_text_segment(text: str):
    segment_endpoint = requests.compat.urljoin(ai21_endpoint, "/studio/v1/segmentation")
    payload = {
        "source": text,
        "sourceType": "TEXT",
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(url=segment_endpoint, json=payload, headers=headers)
    if response.status_code != 200:
        print(response.json())
        return None

    return response.json()


