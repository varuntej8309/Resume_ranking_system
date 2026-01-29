import io
import PyPDF2
from docx import Document

class TextProcessor:
    @staticmethod
    def extract_text(file_stream, filename):
        """Extracts text based on file extension."""
        ext = filename.lower().split('.')[-1]
        
        try:
            if ext == 'txt':
                return file_stream.read().decode('utf-8', errors='ignore')
            elif ext == 'pdf':
                return TextProcessor._extract_from_pdf(file_stream)
            elif ext == 'docx':
                return TextProcessor._extract_from_docx(file_stream)
            else:
                return ""
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            return ""

    @staticmethod
    def _extract_from_pdf(file_stream):
        reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text

    @staticmethod
    def _extract_from_docx(file_stream):
        doc = Document(file_stream)
        return "\n".join([para.text for para in doc.paragraphs])
