from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Session ke liye zaroori hai

LOGO_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRQ0HqT9dk3DeLLbBHebie1wSK7HYWCudOCw&s"

@app.route('/', methods=['GET', 'POST'])
def send_sms():
    if request.method == 'POST':
        session['mobile'] = request.form['mobile']
        session['senderId'] = request.form['senderId']
        session['contentId'] = request.form['contentId']
        session['teleMid'] = request.form['teleMid']
        session['entityId'] = request.form['entityId']
        session['message'] = request.form['message']

        api_url = f"https://bulksmsapi.smartping.ai//?username=cpttest&password=cpttest@888&messageType=text&mobile={session['mobile']}&senderId={session['senderId']}&ContentID={session['contentId']}&TeleMID={session['teleMid']}&EntityID={session['entityId']}&message={session['message']}"
        
        response = requests.get(api_url)
        return f"<h2 style='color: green;'>API Response: {response.text}</h2>"  

    return f'''
    <html>
    <head>
        <title>SMS Panel</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #0e0e0e; color: white; text-align: center; margin: 0; padding: 0; }}
            .container {{ width: 90%; max-width: 500px; margin: auto; padding: 20px; background: #1a1a1a; border-radius: 10px; box-shadow: 0px 0px 15px cyan; }}
            input, textarea {{ width: 100%; padding: 10px; margin: 10px 0; border: none; border-radius: 5px; }}
            input[type="submit"] {{ background: cyan; color: black; font-weight: bold; cursor: pointer; width: 100%; }}
            input[type="submit"]:hover {{ background: darkcyan; }}
        </style>
    </head>
    <body>
        <img src="{LOGO_URL}" alt="Logo" style="width: 80px; height: auto; margin-bottom: 20px;">
        <div class="container">
            <h2>Send SMS via API</h2>
            <form method="post">
                <input type="text" name="mobile" placeholder="Mobile Number" value="{session.get('mobile', '')}" required><br>
                <input type="text" name="senderId" placeholder="Sender ID" value="{session.get('senderId', '')}" required><br>
                <input type="text" name="contentId" placeholder="Content ID" value="{session.get('contentId', '')}" required><br>
                <input type="text" name="teleMid" placeholder="TeleMID" value="{session.get('teleMid', '')}" required><br>
                <input type="text" name="entityId" placeholder="Entity ID" value="{session.get('entityId', '')}" required><br>
                <textarea name="message" placeholder="Enter your message here" required>{session.get('message', '')}</textarea><br>
                <input type="submit" value="Send SMS">
            </form>
        </div>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
