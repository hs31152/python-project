from flask import Flask, request
import datetime
import pytz
import time
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Define username and password
users = {
    "admin": "780740"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None


def epoch_time():
    try:
        # Get TAI time (International Atomic Time)
        tai_time = time.time() + 37  # TAI offset from UTC is currently 37 seconds
        return int(tai_time)
    except Exception as e:
        print(f"Error getting TAI time: {e}")
        return None

def epoch_to_date(epoch_time):
    try:
        ist_timezone = pytz.timezone('Asia/Kolkata')  # IST timezone
        ist_datetime = datetime.datetime.fromtimestamp(epoch_time, ist_timezone)
        human_readable_date = ist_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return human_readable_date
    except Exception as e:
        print(f"Error converting epoch time: {e}")
        return None

def date_to_epoch(human_date):
    try:
        ist_timezone = pytz.timezone('Asia/Kolkata')  # IST timezone
        ist_datetime = datetime.datetime.strptime(human_date, '%Y-%m-%d %H:%M:%S')
        epoch_time = int(ist_datetime.timestamp())
        return epoch_time
    except ValueError as ve:
        print(f"Error converting date to epoch time: {ve}")
        return None

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Epoch and Human-Readable Date Converter</title>
        <style>
            body {
                background: linear-gradient(to right, #4facfe, #00f2fe);
                font-family: 'Arial', sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            .container {
                background-color: rgba(255, 255, 255, 0.9);
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                text-align: center;
                max-width: 80%;
                width: 100%;
                position: relative;
                animation: fadeIn 1s ease;
                margin-top: 20px;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            h2 {
                color: #343a40;
                margin-bottom: 20px;
                font-size: 24px;
                animation: highlight 1s ease-in-out infinite alternate;
            }
            @keyframes highlight {
                from { color: #343a40; }
                to { color: #007bff; }
            }
            input[type="text"] {
                width: calc(100% - 20px);
                padding: 12px;
                margin-bottom: 20px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 16px;
                box-sizing: border-box;
                transition: border-color 0.3s ease;
            }
            input[type="text"]:focus {
                border-color: #007bff;
            }
            input[type="submit"] {
                background-color: #007bff;
                color: #fff;
                border: none;
                padding: 12px 20px;
                text-align: center;
                font-size: 16px;
                border-radius: 4px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                width: 100%;
            }
            input[type="submit"]:hover {
                background-color: #0056b3;
            }
            p {
                color: #6c757d;
                margin-top: 10px;
            }
            a {
                color: #007bff;
                text-decoration: none;
                transition: color 0.3s ease;
            }
            a:hover {
                color: #0056b3;
            }
            .epoch-info {
                max-width: 80%;
                margin-top: 50px;
                padding: 20px;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                animation: fadeIn 1s ease;
            }
            .clock {
                background-color: rgba(255, 255, 255, 0.9);
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                text-align: center;
                max-width: 80%;
                width: 100%;
                position: relative;
                animation: fadeIn 1s ease;
                margin-bottom: 20px;
            }
            @media (max-width: 768px) {
                .container {
                    max-width: 95%;
                }
                .epoch-info {
                    max-width: 95%;
                }
            }
        </style>
    </head>
    <body>
        <div class="clock">
            <h2>Current Epoch Time (TAI): <span id="epoch_clock"></span></h2>
        </div>
        <div class="container">
            <h2>Epoch and Human-Readable Date Converter</h2>
            <form method="post">
                <input type="text" id="epoch_time" name="epoch_time" placeholder="Enter Epoch Time (seconds since epoch)"><br><br>
                <input type="text" id="human_date" name="human_date" placeholder="Enter Human-Readable Date (YYYY-MM-DD HH:MM:SS)"><br><br>
                <input type="submit" value="Convert">
            </form>
        </div>
        <div class="epoch-info">
            <h3>What is Epoch Time?</h3>
            <p>The Unix epoch (or Unix time or POSIX time or Unix timestamp) is the number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT), not counting leap seconds (in ISO 8601: 1970-01-01T00:00:00Z). It is used widely in computing systems for timestamping events.</p>
            <p>Here are some conversions for human-readable time:</p>
            <ul>
                <li>1 hour = 3600 seconds</li>
                <li>1 day = 86400 seconds</li>
                <li>1 week = 604800 seconds</li>
                <li>1 month (30.44 days) = 2629743 seconds</li>
                <li>1 year (365.24 days) = 31556926 seconds</li>
            </ul>
        </div>
        <script>
            function updateEpochTime() {
                fetch('/epoch_time')
                    .then(response => response.text())
                    .then(epoch => {
                        document.getElementById('epoch_clock').textContent = epoch;
                    });
            }
            
            // Update the clock every second
            setInterval(updateEpochTime, 1000);
            
            // Initial update
            updateEpochTime();
        </script>
    </body>
    </html>
    """

    if request.method == 'POST':
        try:
            if 'epoch_time' in request.form and request.form['epoch_time']:
                epoch_time_input = int(request.form['epoch_time'])
                human_date = epoch_to_date(epoch_time_input)
                if human_date:
                    result_html = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Conversion Result</title>
                        <style>
                            body {{
                                background: linear-gradient(to right, #4facfe, #00f2fe);
                                font-family: 'Arial', sans-serif;
                                display: flex;
                                flex-direction: column;
                                justify-content: space-between;
                                align-items: center;
                                min-height: 100vh;
                                margin: 0;
                                padding: 20px;
                            }}
                            .container {{
                                background-color: rgba(255, 255, 255, 0.9);
                                padding: 30px;
                                border-radius: 8px;
                                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                                text-align: center;
                                max-width: 80%;
                                width: 100%;
                                position: relative;
                                animation: fadeIn 1s ease;
                            }}
                            @keyframes fadeIn {{
                                from {{ opacity: 0; }}
                                to {{ opacity: 1; }}
                            }}
                            h2 {{
                                color: #343a40;
                                margin-bottom: 20px;
                                font-size: 24px;
                                animation: highlight 1s ease-in-out infinite alternate;
                            }}
                            @keyframes highlight {{
                                from {{ color: #343a40; }}
                                to {{ color: #007bff; }}
                            }}
                            input[type="text"] {{
                                width: calc(100% - 20px);
                                padding: 12px;
                                margin-bottom: 20px;
                                border: 1px solid #ced4da;
                                border-radius: 4px;
                                font-size: 16px;
                                box-sizing: border-box;
                                transition: border-color 0.3s ease;
                            }}
                            input[type="text"]:focus {{
                                border-color: #007bff;
                            }}
                            p {{
                                color: #6c757d;
                                margin-top: 10px;
                            }}
                            a {{
                                color: #007bff;
                                text-decoration: none;
                                transition: color 0.3s ease;
                            }}
                            a:hover {{
                                color: #0056b3;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h2>Converted Human-Readable Date:</h2>
                            <p>{human_date}</p>
                            <a href="/">Convert Another</a>
                        </div>
                    </body>
                    </html>
                    """
                    return result_html
                else:
                    return "Error converting epoch time."
        except Exception as e:
            print(f"Error processing form: {e}")
            return "Error processing form."

    return html

@app.route('/epoch_time')
@auth.login_required
def get_epoch_time():
    epoch = epoch_time()
    if epoch:
        return str(epoch)
    else:
        return "Error getting epoch time."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)