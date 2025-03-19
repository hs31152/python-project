from flask import Flask, request, render_template_string, redirect, url_for
import pandas as pd
import os
import re

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['UPLOAD_SCRUBBING_FOLDER'] = 'uploadscrubbing'
app.config['UPLOAD_XAG_FOLDER'] = 'upload2'

for folder in [app.config['UPLOAD_FOLDER'], app.config['UPLOAD_SCRUBBING_FOLDER'], app.config['UPLOAD_XAG_FOLDER']]:
    if not os.path.exists(folder):
        os.makedirs(folder)

upload_form_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Morning Reports</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #dc3545;  /* Red color */
        }
        .btn-custom {
            background-color: #dc3545;  /* Red color */
            color: #fff;
            border: none;
        }
        .btn-custom:hover {
            background-color: #c82333;  /* Darker red */
        }
        .file-input-container {
            position: relative;
            margin: 20px 0;
        }
        .file-input {
            position: absolute;
            top: 0;
            left: 0;
            opacity: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
        }
        .file-label {
            display: inline-block;
            background-color: #dc3545;  /* Red color */
            color: white;
            padding: 5px 15px;
            border-radius: 5px;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s, transform 0.3s;
            font-size: 14px;  /* Smaller font size for the label */
        }
        .file-label:hover {
            background-color: #c82333;  /* Darker red */
            transform: scale(1.05);
        }
        .file-label:active {
            transform: scale(0.95);
        }
        .file-name {
            margin-top: 5px;
            font-size: 14px;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container animate__animated animate__fadeIn">
        <h1 class="text-center">Upload Files</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <div class="form-group file-input-container">
                <label for="file1" class="file-label">Choose first file (Excel or CSV)</label>
                <input type="file" id="file1" name="file1" accept=".xlsx, .csv" class="file-input" required>
                <div id="file1-name" class="file-name"></div>
            </div>
            <div class="form-group file-input-container">
                <label for="file2" class="file-label">Choose second file (Excel or CSV)</label>
                <input type="file" id="file2" name="file2" accept=".xlsx, .csv" class="file-input">
                <div id="file2-name" class="file-name"></div>
            </div>
            <div class="form-group file-input-container">
                <label for="file3" class="file-label">Choose third file (Excel or CSV)</label>
                <input type="file" id="file3" name="file3" accept=".xlsx, .csv" class="file-input">
                <div id="file3-name" class="file-name"></div>
            </div>
            <div class="form-group file-input-container">
                <label for="file4" class="file-label">Choose fourth file (Excel or CSV)</label>
                <input type="file" id="file4" name="file4" accept=".xlsx, .csv" class="file-input">
                <div id="file4-name" class="file-name"></div>
            </div>
            <button type="submit" class="btn btn-custom btn-block">Upload</button>
        </form>
        <hr>
        <h1 class="text-center">Upload XAG/Pinnacle Files</h1>
        <form action="/upload_xag_pinnacle" method="post" enctype="multipart/form-data">
            <div class="form-group file-input-container">
                <label for="xag_pinnacle_file" class="file-label">Choose XAG/Pinnacle file (Excel or CSV)</label>
                <input type="file" id="xag_pinnacle_file" name="xag_pinnacle_file" accept=".xlsx, .csv" class="file-input" required>
                <div id="xag_pinnacle-file-name" class="file-name"></div>
            </div>
            <button type="submit" class="btn btn-custom btn-block">Upload XAG/Pinnacle File</button>
        </form>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script>
        document.getElementById('file1').addEventListener('change', function() {
            document.getElementById('file1-name').textContent = this.files.length > 0 ? this.files[0].name : '';
        });
        document.getElementById('file2').addEventListener('change', function() {
            document.getElementById('file2-name').textContent = this.files.length > 0 ? this.files[0].name : '';
        });
        document.getElementById('file3').addEventListener('change', function() {
            document.getElementById('file3-name').textContent = this.files.length > 0 ? this.files[0].name : '';
        });
        document.getElementById('file4').addEventListener('change', function() {
            document.getElementById('file4-name').textContent = this.files.length > 0 ? this.files[0].name : '';
        });
        document.getElementById('xag_pinnacle_file').addEventListener('change', function() {
            document.getElementById('xag_pinnacle-file-name').textContent = this.files.length > 0 ? this.files[0].name : '';
        });
    </script>
</body>
</html>
"""

result_html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Result</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #dc3545;  /* Red color */
        }
        table {
            width: 100%;
            margin: 20px 0;
        }
        .btn-custom {
            background-color: #dc3545;  /* Red color */
            color: #fff;
            border: none;
        }
        .btn-custom:hover {
            background-color: #c82333;  /* Darker red */
        }
        .total-row {
            font-weight: bold;
            background-color: #f8f9fa;
        }
    </style>
</head>
<body>
    <div class="container animate__animated animate__fadeIn">
        <h1 class="text-center">Result</h1>
        <div class="mb-4">
            <h3>Uploaded Files:</h3>
            <ul>
                {% for file_name in file_names %}
                    <li>{{ file_name }}</li>
                {% endfor %}
            </ul>
        </div>
        {{ result_html|safe }}
        <br>
        <a href="/" class="btn btn-custom btn-block">Upload more files</a>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
"""

@app.route('/')
def upload_form():
    return render_template_string(upload_form_html)

@app.route('/upload', methods=['POST'])
def upload_file():

    file_paths = []
    files = [request.files.get('file1'), request.files.get('file2'), request.files.get('file3'), request.files.get('file4')]
    
    for file in files:
        if file and file.filename:
            file_path = os.path.join(app.config['UPLOAD_SCRUBBING_FOLDER'], file.filename)
            file.save(file_path)
            file_paths.append(file_path)
    

    combined_df = pd.DataFrame()
    file_names = []

    for file_path in file_paths:
        file_names.append(os.path.basename(file_path))  
        try:
            if file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path)

            if df.shape[1] == 1:
                df.columns = ['Combined']
                
                df[['Value', 'Filename']] = df['Combined'].str.extract(r'(\d+)\s+(.+)')
                df['Value'] = pd.to_numeric(df['Value'], errors='coerce').fillna(0)
                df.drop(columns=['Combined'], inplace=True)
                
                def extract_cdr_type(filename):
                    parts = filename.split('_')
                    return parts[1] if len(parts) > 1 else 'Unknown'
                
                df['cdr_type'] = df['Filename'].apply(extract_cdr_type)

                combined_df = pd.concat([combined_df, df], ignore_index=True)
            else:
                return "One of the files does not contain the expected single column format."

        except Exception as e:
            return f"An error occurred with one of the files: {str(e)}"

    if not combined_df.empty:
        result = combined_df.groupby('cdr_type')['Value'].sum().reset_index()
        result.columns = ['cdr_type', 'Total Value']

        specific_cdr_types = ['250', '251', '123', '126', '243', '247', '244', '120', '127' ]
        result = result.set_index('cdr_type').reindex(specific_cdr_types, fill_value=0).reset_index()
        result.columns = ['cdr_type', 'Total Value']

        result['cdr_type'] = result['cdr_type'].replace({'250': '250 (progate)', '251': '251 (RML)'})

        result_for_total = result[~result['cdr_type'].isin(['250 (progate)', '251 (RML)'])]
        total_value = result_for_total['Total Value'].sum()

        total_row = pd.DataFrame({'cdr_type': ['Total value of scrubbing excluding Progate and RML'], 'Total Value': [total_value]})
        result = pd.concat([result, total_row], ignore_index=True)

        result_html = result.to_html(index=False, classes='table table-striped table-bordered')
        
        return render_template_string(result_html_template, result_html=result_html, file_names=file_names)

    return "No valid data found in the uploaded files."

@app.route('/upload_xag_pinnacle', methods=['POST'])
def upload_xag_pinnacle_file():
    file = request.files.get('xag_pinnacle_file')
    if file and file.filename:
        file_path = os.path.join(app.config['UPLOAD_XAG_FOLDER'], file.filename)
        file.save(file_path)

        if file_path.endswith('.csv'):
            read_func = pd.read_csv
        elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            read_func = pd.read_excel
        else:
            return '''
            <html>
            <body>
                <h1>Error</h1>
                <p>Only CSV and Excel files are supported. Please upload a valid CSV or Excel file.</p>
                <a href="/">Upload Another File</a>
            </body>
            </html>
            '''

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, delimiter=r'\s+', header=None)
            else:
                df = pd.read_excel(file_path, header=None)

            if df.shape[1] < 2:
                raise ValueError("The file does not have enough columns.")

            df.columns = ['value', 'category']

            df['value'] = pd.to_numeric(df['value'], errors='coerce')

            df = df.dropna(subset=['value'])

            df['value'] = df['value'].astype(int)

            df['category_code'] = df['category'].apply(lambda x: re.search(r'\d{4}', x).group() if re.search(r'\d{4}', x) else 'unknown')

            xag_sum = df[df['category_code'].isin(['7000', '7001'])]['value'].sum()
            pinnacle_sum = df[df['category_code'].isin([str(i) for i in range(7002, 7010)])]['value'].sum()

            result = f'XAG: {xag_sum}\nPinnacle: {pinnacle_sum}'

            return f'''
            <html>
            <body>
                <h1>Results</h1>
                <pre>{result}</pre>
                <a href="/">Upload Another File</a>
            </body>
            </html>
            '''
        except Exception as e:
            return f'''
            <html>
            <body>
                <h1>Error</h1>
                <p>Failed to process file: {e}</p>
                <a href="/">Upload Another File</a>
            </body>
            </html>
            '''

if __name__ == "__main__":
    app.run()
    
