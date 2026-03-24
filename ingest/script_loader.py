import os
from docx import Document
from PyPDF2 import PdfReader


class ScriptLoader:

    def load_script(self, file_path):
        """
        Detect file type and load script text.
        """

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".txt":
            return self._load_txt(file_path)

        elif extension == ".docx":
            return self._load_docx(file_path)

        elif extension == ".pdf":
            return self._load_pdf(file_path)

        elif extension == ".srt":
            return self._load_srt(file_path)

        else:
            raise ValueError("Unsupported file format")

    def _load_txt(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def _load_docx(self, file_path):
        doc = Document(file_path)
        text = []

        for paragraph in doc.paragraphs:
            text.append(paragraph.text)

        return "\n".join(text)

    def _load_pdf(self, file_path):
        reader = PdfReader(file_path)
        text = []

        for page in reader.pages:
            text.append(page.extract_text())

        return "\n".join(text)

    def _load_srt(self, file_path):
        text = []

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line.isdigit():
                    continue

                if "-->" in line:
                    continue

                if line != "":
                    text.append(line)

        return "\n".join(text)