import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def analyze_bill_and_plan(image_pil, current_reading, days_left, appliances, language):
    # Retrieve key from environment variable (Rule #8)
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an expert Pakistani electricity (HESCO/WAPDA) tariff advisor.
    1. If an image of a bill is provided, extract the units consumed, tariff slab, and taxes.
    2. Otherwise, use the user's manual reading: {current_reading} units consumed so far, with {days_left} days left in the month.
    3. The user runs these appliances: {', '.join(appliances)}.
    4. Respond in {language}.

    Return ONLY valid JSON with these exact keys:
    {{
        "units_consumed": int,
        "projected_monthly_units": int,
        "current_slab_status": "Safe (Protected)" or "Danger (Near Slab Jump)" or "High Tariff",
        "next_slab_limit": int,
        "estimated_bill_now_pkr": int,
        "estimated_bill_if_slab_crossed_pkr": int,
        "bill_explanation": "2 short sentences explaining their bill & slab risk",
        "daily_schedule": [
            {{"appliance": "string", "advice": "specific tip with hours to avoid peak (6 PM - 10 PM)", "estimated_savings_pkr": int}}
        ]
    }}
    """

    contents = [prompt]
    if image_pil:
        contents.append(image_pil)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        ),
    )
    return json.loads(response.text)
