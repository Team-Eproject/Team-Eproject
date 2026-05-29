import google.generativeai as genai #Geminiをインポート
from IPython.display import display, Markdown
from django.conf import settings


#APIキーの設定
API_KEY = settings.GEMINI_API_KEY

# Geminiの設定
genai.  configure(api_key=API_KEY)

#GeminiAIのインスタンスを生成
model = genai.GenerativeModel('gemini-pro')

#APIを使ってリクエストを投げる
response = model.generate_content(
    prompt = f"""
あなたは優秀な献立メニューアドバイザーです。

入力されるJSONデータをもとに、
指定条件に合った献立を提案してください。

# 入力データ
{request_data}

# 入力データの説明
- foods:
    - name: 食材名
    - quantity: 分量
    - unit: 単位
    - expiration_date: 賞味期限
- menu_count:
    - 提案するメニュー数
- request:
    - ユーザーからの追加要望

# ルール
1. 回答は必ず日本語
2. 賞味期限が近い食材を優先的に使用
3. request の内容を必ず考慮
4. menu_count の数だけ献立を提案
5. 各メニューに以下を含める
    - メニュー名
    - 必要な材料
    - 作り方
6. 作り方は必ず番号付きにする
7. 今日の日付を基準に賞味期限が近い順で優先使用してください
8. 賞味期限切れの食材は使用しないでください
"""
)