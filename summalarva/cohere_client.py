import time
from pathlib import Path

from cohere import Client

from summalarva.pdfextract import extract_pdf


class CohereClient:
    def __init__(self, api_key):
        self.client = Client(api_key)

    def summarize_doc(self, doc_path, model='summarize-xlarge', length='medium', extractiveness='medium'):
        pages = extract_pdf(Path(doc_path).expanduser())
        summarises = []
        count_call = 0
        time_start = time.time()
        # limit 5 call every minute
        for page_num, page in enumerate(pages):
            count_call += 1
            if count_call == 6:
                time_end = time.time()
                period = time_end - time_start
                if period < 60:
                    time.sleep(60 - period)
                time_start = time.time()
                count_call = 0
            print("Start processing page", page_num + 1)
            response = self.client.summarize(page, model=model,
                                             length=length,
                                             extractiveness=extractiveness)
            summarises.append(response.summary)
        return summarises
