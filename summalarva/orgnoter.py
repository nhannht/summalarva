import os
from pathlib import Path
import logging

class OrgNoter:
    """
    This class is used to create orgnoter note
    """
    def __init__(self, doc_path, root="~/org"):
        self.doc_path = Path(doc_path).expanduser()  # relative path to doc with ext "/home/vermin/pdf/abc.pdf"
        self.noter_root = Path(root).expanduser()  # where orgnoter save note "/home/vermin/org"

        self.doc_name = self.doc_path.stem  # name of doc without ext, without path "abc"

        self.note_name = self.doc_name + ".org" # name of note with ext, without path "abc.org"
        self.note_path = self.noter_root.joinpath(self.note_name) # path to note with ext, with path "/home/vermin/org/abc.org"
        self.first_heading = f"""* {self.doc_name}
:PROPERTIES:
:NOTER_DOCUMENT: {self.doc_path}
:NOTER_PAGE: 1
:END:
"""
        self.pages_note = []
        self.second_heading = f"""
** Pages summarize
"""

    def page_summarize_model_append(self, pagenum: int, content: str):
        """

        :param pagenum: The covert or first page start from 1, so ussually this number will start from 1
        :param content:
        :return:
        """
        self.pages_note.append(f"""
*** Page {pagenum} summary
:PROPERTIES:
:NOTER_PAGE: {pagenum}
:END:
{content}
""")
        logging.error(f"Page {pagenum+1} summary appended")

    def create_note(self):
        if not self.noter_root.exists():
            os.makedirs(self.noter_root)
        if not self.note_path.exists():
            with open(self.note_path, "w") as f:
                f.write(self.first_heading)
        with open(self.note_path, "a") as f:
            f.write(self.second_heading)
            f.write("\n".join(self.pages_note))
