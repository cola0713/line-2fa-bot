import os
import time
import pyotp
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 1. LINE 金鑰
LINE_CHANNEL_ACCESS_TOKEN = "9kluz2S3S0ozWaCpHDiaXcVLqBLP2R9fA2I32cAChJy83xYfX6Ag6hlmzf0LiKEqoV/mMTDxCNX38sQ6LufepQq9S7H8W2473WgsGULVASO+vKlnaIMnV6qeuNesscpZiBH0XXuA63E8Rt/ZnyasDwdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "465c50ad6d658554cfac3b9c22b6ee71"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 2. Google 2FA 金鑰（自動去除空格並轉為大寫）
RAW_SECRET = "wwow k54a uqxn 7jkh hqpf 4pmq swd3 vxws"
TOTP_SECRET_KEY = RAW_SECRET.replace(" ", "").upper()

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

    if user_msg.lower() in ['驗證碼', '2fa', 'google', '碼']:
        totp = pyotp.TOTP(TOTP_SECRET_KEY)
        current_code = totp.now()
        
        # 計算 30 秒倒數剩餘秒數
        time_remaining = 30 - (int(time.time()) % 30)

        reply_text = f"🔑 Google 最新驗證碼：\n\n{current_code}\n\n⏱️ 剩餘有效時間：{time_remaining} 秒"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

if __name__ == "__main__":
    app.run(port=5000)
