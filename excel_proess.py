import os
import pandas as pd
from flask import Flask, request, send_file, render_template_string

app = Flask(__name__)

# Get the Downloads folder path
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

# Links and Logo
LOGO_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRQ0HqT9dk3DeLLbBHebie1wSK7HYWCudOCw&s"
INSTAGRAM_URL = "https://instagram.com/harshit__2244"
EMAIL = "mailto:harshitsharma31152@gmail.com"
PHONE = "tel:+918219673715"

def process_excel(input_path, original_filename):
    df = pd.read_excel(input_path)

    # Remove 'Source' column if it exists
    if "Source" in df.columns:
        df = df.drop(columns=["Source"])

    # Reshape the data: Convert wide format to long format
    df_grouped = df.melt(id_vars=["Date"], var_name="Code", value_name="Count")

    # Aggregate duplicate 'Code' values per date
    df_grouped = df_grouped.groupby(["Date", "Code"], as_index=False).sum()

    # Pivot table to arrange data in the required format
    df_pivot = df_grouped.pivot(index="Code", columns="Date", values="Count")

    # Reset index for better structure
    df_pivot.reset_index(inplace=True)

    # Create formatted filename
    filename_without_ext = os.path.splitext(original_filename)[0]
    output_filename = f"{filename_without_ext}_formatted_data.xlsx"

    # Save the formatted data in Downloads folder
    output_path = os.path.join(DOWNLOADS_FOLDER, output_filename)
    df_pivot.to_excel(output_path, index=False)

    return output_filename  # Return file name only

@app.route('/')
def upload_form():
    return render_template_string(HTML_TEMPLATE, LOGO_URL=LOGO_URL, INSTAGRAM_URL=INSTAGRAM_URL, EMAIL=EMAIL, PHONE=PHONE)

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    original_filename = file.filename  # Get original file name
    input_path = "temp_uploaded_file.xlsx"
    file.save(input_path)
    
    output_filename = process_excel(input_path, original_filename)

    return render_template_string(HTML_TEMPLATE, success=True, filename=output_filename, uploaded_filename=original_filename, LOGO_URL=LOGO_URL, INSTAGRAM_URL=INSTAGRAM_URL, EMAIL=EMAIL, PHONE=PHONE)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(DOWNLOADS_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload & Process Excel</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
            text-align: center;
        }
        .container {
            background: rgba(255, 255, 255, 0.15);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            max-width: 500px;
            width: 90%;
        }
        .logo {
            width: 100px;
            height: 100px;
            margin-bottom: 15px;
            border-radius: 50%;
        }
        h1 {
            margin-bottom: 20px;
        }
        input[type="file"] {
            display: none;
        }
        label {
            background: #ff8c00;
            padding: 12px 24px;
            cursor: pointer;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s;
            display: block;
        }
        label:hover {
            background: #ff6f00;
        }
        .file-name {
            margin-top: 10px;
            font-size: 14px;
            color: #ffcc00;
            font-weight: 500;
        }
        button {
            margin-top: 15px;
            background: #28a745;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s;
        }
        button:hover {
            background: #218838;
        }
        .download-btn {
            margin-top: 20px;
            display: block;
            background: #007bff;
            padding: 12px 24px;
            text-decoration: none;
            color: white;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
        }
        .download-btn:hover {
            background: #0056b3;
        }
        .success-message {
            margin-top: 15px;
            color: #00ff99;
            font-weight: bold;
        }
        .footer {
            margin-top: 30px;
            font-size: 14px;
        }
        .footer a {
            color: #ffcc00;
            text-decoration: none;
            margin: 0 10px;
        }
        .footer a:hover {
            color: #ff9900;
        }
    </style>
</head>
<body>
    <div class="container">
        <img src="{{ LOGO_URL }}" alt="Logo" class="logo">
        <h1>Excel Processor</h1>
        <form method="POST" action="/process" enctype="multipart/form-data">
            <input type="file" name="file" id="fileInput" onchange="updateFileName()">
            <label for="fileInput">Choose File</label>
            <p class="file-name" id="fileName">No file chosen</p>
            <button type="submit">Upload & Process</button>
        </form>
        {% if success %}
            <p class="success-message">File Processed Successfully!</p>
            <p class="file-name">Uploaded: {{ uploaded_filename }}</p>
            <a href="/download/{{ filename }}" class="download-btn">Download Processed File</a>
        {% endif %}
    </div>
    <div class="footer">
        <p>Connect with me:</p>
        <a href="{{ INSTAGRAM_URL }}" target="_blank">Instagram</a> |
        <a href="{{ EMAIL }}">Email</a> |
        <a href="{{ PHONE }}">Phone</a>
    </div>
    <script>
        function updateFileName() {
            var input = document.getElementById('fileInput');
            var fileName = document.getElementById('fileName');
            fileName.textContent = input.files.length > 0 ? input.files[0].name : "No file chosen";
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
