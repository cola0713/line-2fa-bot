import os
import pyotp
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 1. 填入你的 LINE Bot 金鑰 (也可以設定在環境變數中)
LINE_CHANNEL_ACCESS_TOKEN = "9kluz2S3S0ozWaCpHDiaXcVLqBLP2R9fA2I32cAChJy83xYfX6Ag6hlmzf0LiKEqoV/mMTDxCNX38sQ6LufepQq9S7H8W2473WgsGULVASO+vKlnaIMnV6qeuNesscpZiBH0XXuA63E8Rt/ZnyasDwdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "465c50ad6d658554cfac3b9c22b6ee71"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 2. 填入你的 Google 2FA 文字金鑰 (Secret Key)
TOTP_SECRET_KEY = "JBSWY3DPEHPK3PXP" # 替換成你們團隊的實際金鑰

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 LINE 傳來的 HTTP 標頭與內文
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 當使用者在 LINE 傳送文字訊息時觸發
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text.strip()

    # 當隊員傳送「驗證碼」、「2fa」或點擊選單按鈕時觸發
    if user_msg.lower() in ['驗證碼', '2fa', 'google', '碼']:
        # 即時計算當前最新的 6 位數驗證碼
        totp = pyotp.TOTP(TOTP_SECRET_KEY)
        current_code = totp.now()

        # 算出這組驗證碼還剩多少秒過期 (TOTP 30 秒一期)
        time_remaining = 30 - (int(totp.time()) % 30)

        reply_text = f"🔑 Google 最新驗證碼：\n\n{current_code}\n\n⏱️ 剩餘有效時間：{time_remaining} 秒"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

if __name__ == "__main__":
    app.run(port=5000)