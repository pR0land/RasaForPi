import requests

sender = input("Hvad hedder du?\n")

bot_message = ""
while bot_message != "Farvel":
    message = input("What's your message?\n")

    print("Sending message now..")

    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message":"Hej"})

    print("Bot says, ",end=' ')
    for i in r.json():
        bot_message = i['text']
        print(f"{i['text']}")

