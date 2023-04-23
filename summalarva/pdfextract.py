# extract pdf page by page and store in list
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from pathlib import Path
import tiktoken
file = Path('/home/vermin/IdeaProjects/summalarva/output.pdf')
encoder = tiktoken.encoding_for_model("text-davinci-003")


def extract_pdf(file):
    pages = []
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(file, 'rb')
    for page_number, page in enumerate(PDFPage.get_pages(fp)):
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        interpreter.process_page(page)
        data = retstr.getvalue()
        pages.append(data)
        retstr.truncate(0)
        retstr.seek(0)
    return pages


