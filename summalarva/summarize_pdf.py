#!/usr/bin/env python3
import argparse
import configparser
from pathlib import Path

from rich import console

import sys
sys.path.append("/home/vermin/IdeaProjects/summalarva")
from summalarva.openai_client import OpenAIClient
from summalarva.orgnoter import OrgNoter

console = console.Console()
config = configparser.ConfigParser()
argparser = argparse.ArgumentParser()
argparser.add_argument("input", type=str, help="Input file")
argparser.add_argument("--config", type=str, help="Config file")
args = argparser.parse_args()
input_path = Path(args.input).expanduser()

if args.config:
    config.read(args.config)
else:
    config.read(Path("~/.config/summalarva.ini").expanduser())

openai_api_key = config["openai"]["api_key"]
if config["openai"]["host"]:
    openai_host = config["openai"]["host"]
    openai_client = OpenAIClient(openai_api_key, openai_host)
else:
    openai_client = OpenAIClient(openai_api_key)

console.print("Start processing file", args.input)
summarises = openai_client.summarize_document(args.input)
try:
    org_noter = OrgNoter(args.input)
    for page_num,summary in summarises.items():
        org_noter.page_summarize_model_append(page_num, summary)
    console.print("Start create org noter")
    org_noter.create_note()
except Exception as e:
    raise e


summary_text = ""
for page_num, summary in summarises.items():
    summary_text += f"Page {page_num}\n\n{summary}\n\n"

with open("summary.txt", "w") as f:
    f.write(summary_text)






