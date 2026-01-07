from agents.llm import ask_gemini
from agents.clean_json import clean_json
import json


def notes_agent(ocr_result: list):
    """
    Uses LLM to summarize the file summary
    """
    prompt = f""" 
        You are a notes summarizer agent.

For EACH file, generate:
- title
- summary
- key_points
- formulas

Return JSON ONLY in this format:

{{
  "filename1": {{
    "title": "...",
    "summary": "...",
    "key_points": [],
    "formulas": []
  }}
}}


        OCR Result: 
        \"\"\"{ocr_result}\"\"\"

  """
    response = ask_gemini(prompt)
    try:
        print("gemini result: ", response)
    except:
        print("NONE response")
    response = clean_json(response)
    
    return json.loads(response)

