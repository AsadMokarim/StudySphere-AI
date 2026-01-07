import re
import json

def clean_json(response: str) -> str:
    """
    Cleans LLM response to extract valid JSON
    """
    if not response:
        print("WARNING: Empty response received")
        return "{}"
    
    # Remove markdown code blocks
    response = re.sub(r'```json\s*', '', response)
    response = re.sub(r'```\s*', '', response)
    
    # Remove any leading/trailing whitespace
    response = response.strip()
    
    # If response starts with explanatory text, try to find JSON
    if not response.startswith('{') and not response.startswith('['):
        # Try to find JSON object
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            response = match.group(0)
        else:
            # Try to find JSON array
            match = re.search(r'\[.*\]', response, re.DOTALL)
            if match:
                response = match.group(0)
            else:
                print(f"WARNING: No JSON found in response: {response[:100]}")
                return "{}"
    
    # Validate it's actually JSON before returning
    try:
        json.loads(response)  # Test if valid
        return response
    except json.JSONDecodeError as e:
        print(f"WARNING: Invalid JSON after cleaning: {e}")
        print(f"First 200 chars: {response[:200]}")
        return "{}"