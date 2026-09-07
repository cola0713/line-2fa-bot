import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# LINE 金鑰設定
LINE_CHANNEL_ACCESS_TOKEN = "9kluz2S3S0ozWaCpHDiaXcVLqBLP2R9fA2I32cAChJy83xYfX6Ag6hlmzf0LiKEqoV/mMTDxCNX38sQ6LufepQq9S7H8W2473WgsGULVASO+vKlnaIMnV6qeuNesscpZiBH0XXuA63E8Rt/ZnyasDwdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "465c50ad6d658554cfac3b9c22b6ee71"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text.strip()
    msg_lower = user_msg.lower()

    # -----------------------------------------------------------
    # 活動資訊問答（可依需求修改或新增）
    # -----------------------------------------------------------
    if '這個活動是幹嘛的' in user_msg or '活動介紹' in user_msg or '活動內容' in user_msg:
        reply_text = (
            "🎉 【最新活動介紹】\n\n"
            "歡迎參加我們的宣傳推廣活動！本次活動主要提供全新的體驗與好康福利。\n\n"
            "📌 活動重點：\n"
            "1. 了解最新產品與服務內容\n"
            "2. 完成指定任務即可獲得專屬獎勵\n\n"
            "如需更多細節，歡迎直接留言詢問小幫手！"
        )

    elif '報名' in user_msg or '怎麼參加' in user_msg:
        reply_text = "👉 請點擊以下連結填寫報名表單：\nhttps://example.com/register"

    elif '時間' in user_msg or '地點' in user_msg:
        reply_text = "📅 活動時間：即日起至月底止\n📍 活動地點：線上進行 / 詳見官方網站公告"

    # -----------------------------------------------------------
    # 預設回覆（當無法匹配以上關鍵字時）
    # -----------------------------------------------------------
    else:
        reply_text = (
            "你好！我是活動小幫手 🤖\n\n"
            "你可以輸入以下關鍵字來取得資訊：\n"
            "🔹 輸入「活動介紹」：了解活動內容\n"
            "🔹 輸入「報名」：取得報名連結\n"
            "🔹 輸入「時間」或「地點」：查詢活動時間與地點"
        )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(port=5000)
