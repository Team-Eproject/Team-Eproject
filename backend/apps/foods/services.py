from google import genai
from .schemas import Menus
from django.conf import settings

def generate_menu(request_data):
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )
    

    prompt = f"""

    ...
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Menus.model_json_schema(),
        },
    )
    
    return Menus.model_validate_json(response.text)