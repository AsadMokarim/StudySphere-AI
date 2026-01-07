from agents.llm import ask_gemini
from agents.clean_json import clean_json
import json

def quiz_agent(notes: list, options: dict):
    quiz_type = options.get("quiz_type", "mcq")
    difficulty = options.get("difficulty", "medium")
    num_questions = options.get("num_questions", 10)

    prompt = f"""
You are a quiz generator agent.

Use the following study notes to generate a quiz:
\"\"\"{notes}\"\"\"

Quiz constraints:
- Type: {quiz_type}
- Difficulty: {difficulty}
- Number of questions: {num_questions}

Return JSON ONLY in this format:

{{{{
  "questions": [
    {{{{
      "id": "Q1",
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": 0
    }}}},
    {{{{
      "id": "Q2",
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": 2
    }}}}
  ]
}}}}

Note: The "answer" field should be an integer index (0-3) indicating which option is correct.
"""

    response = ask_gemini(prompt)
    print("Quiz Gemini raw response:\n", response)

    response = clean_json(response)
    return json.loads(response)