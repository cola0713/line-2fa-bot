import os
import time
import pyotp
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 1. 填入你的 LINE 金鑰
LINE_CHANNEL_ACCESS_TOKEN = '貼上你的 Channel Access Token'
LINE_CHANNEL_SECRET = '貼上你的 Channel Secret'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 2. 填入 Google 2FA 16位數文字金鑰
TOTP_SECRET_KEY = "JBSWY3DPEHPK3PXP" 

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
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
        
        # 使用 Python 內建的 time.time() 計算剩餘秒數，避免 pyotp 屬性錯誤
        time_remaining = 30 - (int(time.time()) % 30)

        reply_text = f"🔑 Google 最新驗證碼：\n\n{current_code}\n\n⏱️ 剩餘有效時間：{time_remaining} 秒"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

if __name__ == "__main__":
    app.run(port=5000)
