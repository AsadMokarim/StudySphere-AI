from agents.llm import ask_gemini
from agents.notes_agent import notes_agent
from PIL import Image
import pytesseract
import io



def ocr_agent(files):
    """
    Agent generates a text, by using ocr capability of pytesseract
    """
    result = []
    for file in files: 
        if not file.content_type.startswith("image/"):
            continue
        
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)

        result.append({
            "filename": file.filename,
            "text": text.strip()
        })
    print(f'result: {result}')
    return result