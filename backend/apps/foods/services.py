imoprt json

from google import genai
from .schemas import Menus
from django.conf import settings

def generate_menu(request_data):
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )
    

    prompt = f"""
    あなたは優秀な献立メニューアドバイザーです。

    以下の条件に従って献立を作成してください。

    # 重要ルール
    - 賞味期限が近い食材を優先して使用して下さい
    - expiration_days が小さいほど優先度が高いです
    - できるだけ食品ロスを減らしてください
    - 同じ食材を使い切るよう工夫してください

    
    # 出力ルール
    必ずJSON形式のみで返してください
    schema に必ず従ってください
    instructions は手順を順番に分けてください
    cooking_time_minutes は整数で返してください

    # 食材情報
    {json.dumps(request_data, ensure_askii=False, indent=2)}


    """

    try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Menus.model_json_schema(),
        },
    )
    
    if not response.text:
        raise ValueError("Gemini response is enpty")

    return Menus.model_validate_json(response.text)

except Exception as e:
    print(f"gemini API Error: {e}")
    return None