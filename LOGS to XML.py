from flask import Flask, render_template_string, request, jsonify
import re

app = Flask(__name__)

# Function to process log data and return the desired output
def process_log(input_log):
    try:
        # Extract all <MSG> blocks using regex
        msg_matches = re.findall(r"<MSG>.*?</MSG>", input_log, re.DOTALL)
        if not msg_matches:
            return "Error: No valid <MSG> blocks found in the input."

        # Process each message block to modify <TYPE> and remove unwanted fields
        processed_msgs = []
        for msg in msg_matches:
            msg = re.sub(r"<USER_ID_1>.*?</USER_ID_1>", "", msg)
            msg = re.sub(r"<RESP_CODE>.*?</RESP_CODE>", "", msg)
            msg = re.sub(r"<CDR_ID>.*?</CDR_ID>", "", msg)
            msg = re.sub(r"<TYPE>.*?</TYPE>", "<TYPE>IN</TYPE>", msg)
            processed_msgs.append(msg)

        sorted_msg_matches = sorted(processed_msgs, key=lambda x: re.search(r"<SMS_ID>(.*?)</SMS_ID>", x).group(1))

        output = "\n".join([f'msglist.append("{msg.strip()}")' for msg in sorted_msg_matches])
        return output
    except Exception as e:
        return f"Error occurred: {str(e)}"

@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Log Processor</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #1a1a2e, #16213e);
                    color: #fff;
                    text-align: center;
                }
                .container {
                    width: 80%;
                    margin: 5% auto;
                    padding: 20px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    box-shadow: 0px 0px 15px rgba(0, 255, 255, 0.2);
                    backdrop-filter: blur(10px);
                    animation: fadeIn 1s ease-in-out;
                }
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(-10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                textarea {
                    width: 100%;
                    height: 150px;
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 8px;
                    border: none;
                    background: rgba(255, 255, 255, 0.2);
                    color: #fff;
                    font-size: 14px;
                }
                textarea::placeholder {
                    color: rgba(255, 255, 255, 0.7);
                }
                button {
                    background: linear-gradient(45deg, #00c6ff, #0072ff);
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    transition: all 0.3s ease-in-out;
                    animation: pulse 1.5s infinite;
                }
                @keyframes pulse {
                    0% { box-shadow: 0 0 5px #00c6ff; }
                    50% { box-shadow: 0 0 20px #00c6ff; }
                    100% { box-shadow: 0 0 5px #00c6ff; }
                }
                button:hover {
                    transform: scale(1.1);
                    background: linear-gradient(45deg, #0072ff, #00c6ff);
                }
                .output-box {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 10px;
                    border-radius: 5px;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    font-family: monospace;
                    font-size: 14px;
                    color: #fff;
                    margin-top: 20px;
                    max-height: 300px;
                    overflow-y: auto;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Log Processor</h1>
                <form id="logForm">
                    <label for="input_log">Enter Input Logs:</label><br>
                    <textarea id="input_log" name="input_log" placeholder="Enter log data here"></textarea><br>
                    <button type="submit">Process</button>
                </form>
                <div class="output-box">
                    <div class="output-title">Processed Output:</div>
                    <pre id="output"></pre>
                </div>
            </div>
            <script>
                document.getElementById('logForm').onsubmit = function(event) {
                    event.preventDefault();
                    let logData = document.getElementById('input_log').value;
                    fetch('/process', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({input_log: logData})
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('output').textContent = data.output;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('output').textContent = 'Error processing the log.';
                    });
                };
            </script>
        </body>
        </html>
    """)

@app.route('/process', methods=['POST'])
def process():
    input_log = request.json.get('input_log', '')
    result = process_log(input_log)
    return jsonify({"output": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
