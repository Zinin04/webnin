from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json,urllib.request
import os
import json

app = Flask(__name__)
line_bot_api = LineBotApi('7lEmSpbK7oSY7sq6Du5i1GmhoMQwzrz4VJhBVRoSlCyFCa1Yc2mgdNKNTWWDMZwHYyZUZgxGAqw79z9kFbfrMOpkhu4mXtmvav/wF1+ui1A6m3fFA4yqH5/VmQkascQHeQox8J7KJwzLCqQDUmrRVgdB04t89/1O/w1cDnyilFU=')
line_handler = WebhookHandler('af034d8a0d6d2be041ec35049ca6231a')

url ='https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-FE12EF11-E162-46C5-B1E4-A3FC8ACA714B&format=JSON'
ansA=[]
city=''

@app.route('/')
def home():
    return 'Hello World!'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


def myG(aa):
    ansA.clear()
    data = urllib.request.urlopen(url).read()
    output = json.loads(data)
    location=output['records']['location']
    for i in location:
        city = i['locationName']
        if city==aa:
            wx = i['weatherElement'][0]['time'][0]['parameter']['parameterName']
            maxtT = i['weatherElement'][4]['time'][0]['parameter']['parameterName']
            mintT = i['weatherElement'][2]['time'][0]['parameter']['parameterName']
            ci = i['weatherElement'][3]['time'][0]['parameter']['parameterName']
            pop = i['weatherElement'][4]['time'][0]['parameter']['parameterName']
            
            ansA.append(city)
            ansA.append(wx)
            ansA.append(mintT)
            ansA.append(maxtT)
    return ansA



@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):        

    if event.message.text == "1":        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(myG('臺北市'))))        

    elif event.message.text == "2":        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(myG('桃園市'))))
        
    elif event.message.text=='3':            
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(myG('新竹市'))))
        
    elif event.message.text=='4':            
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(myG('臺中市'))))
        
    elif event.message.text=='5':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(myG('臺南市'))))
        
    elif event.message.text=='6':            
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(myG('高雄市'))))
        
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="只有1-6的數字"))

if __name__ == "__main__":
    app.run()
