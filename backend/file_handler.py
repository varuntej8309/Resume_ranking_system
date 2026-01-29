import io
from .text_processor import TextProcessor

class FileHandler:
    @staticmethod
    def process_uploads(files):
        """Processes a list of file objects into a text corpus."""
        processed_data = []
        
        for file in files:
            # Skip entries with no filename
            if not file or not file.filename:
                continue
                
            try:
                # CRITICAL: Always reset the file pointer to the beginning
                file.seek(0)
                file_content = file.read()
                
                # Double check content length
                if not file_content:
                    print(f"Warning: File {file.filename} appears to be empty.")
                    continue
                
                # Pass to text processor as a fresh stream
                text = TextProcessor.extract_text(io.BytesIO(file_content), file.filename)
                
                if text and len(text.strip()) > 10: # Minimum text requirement
                    processed_data.append({
                        'filename': file.filename,
                        'text': text
                    })
                else:
                    print(f"Warning: No meaningful text found in {file.filename}")
                    
            except Exception as e:
                print(f"Error handling file {file.filename}: {str(e)}")
                continue
                
        return processed_data
