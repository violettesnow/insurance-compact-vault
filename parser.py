import os
from google import genai
from google.genai import types

# Setup: Get your API Key from aistudio.google.com
client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

def parse_insurance_pdf(pdf_path):
    """
    Sends the PDF directly to Gemini-3-Flash for 'Vision-based' table extraction.
    This bypasses traditional text-parsing issues with insurance table layouts.
    """
    print(f"📄 Parsing {pdf_path} using Vision LLM...")
    
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    # The 'Prompt' is the Schema
    prompt = """
    Extract the insurance rating tables from this document into a structured JSON.
    I need three specific objects:
    1. 'base_rates': The starting annual premium for Atlanta (Zip 30303).
    2. 'driver_multipliers': Multipliers for Age, Gender, and Marital Status.
    3. 'vehicle_symbols': The risk multipliers for common car years/makes/models.

    Format the response as a valid JSON object. If a value is missing, use null.
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview", # Flash is optimized for speed/extraction
        contents=[
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
            prompt
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json", # Forces valid JSON output
        )
    )
    
    return response.text

# Example usage for your hackathon test
if __name__ == "__main__":
    # You would pass a PDF path downloaded by your engine.py here
    # result = parse_insurance_pdf("state_farm_ga_2026.pdf")
    # print(result)
    pass
