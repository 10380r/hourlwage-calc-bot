from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import calc
import os


app = Flask(__name__)

secret = "LINE_CHANNEL_SECRET"
token  = "LINE_CHANNEL_ACCESS_TOKEN"
line_bot_api = LineBotApi(secret)
print(secret)
handler = WebhookHandler(token)
print(token)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        salary = call_calc(event.message.text)
        reply = 'あんたの今日のお給料はね、\n￥%sだな。\nお疲れ✋' %(salary)
    except:
        reply = '''\
%s? \n
ちゃんとしたフォーマットで返答しろやアホ

ちゃんとしたフォーマット-------
曜日     (ex.土, 土曜)
時給     (ex.1000)
開始時刻 (ex.18:00)
終了時刻 (ex.24:00)
-------------------------------
''' %(event.message.text)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))


def call_calc(message):
    l = message.splitlines()
    day    = l[0]
    hourly = l[1]
    start  = l[2]
    end    = l[3]
    return calc.calc(start, end, day, hourly)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
