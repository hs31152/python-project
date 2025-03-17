import os
import pandas as pd
from flask import Flask, render_template_string, request, send_file

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LA.🤡.LA.🤡.LA.🤡.LA.🤡</title>
    <style>
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        body { font-family: "Times New Roman", Times, serif; margin: 20px; background: linear-gradient(135deg,rgb(216, 143, 143),rgb(164, 164, 240)); text-align: center; }
        h2 { animation: bounce 1s infinite; color:rgb(45, 0, 87); }
        form { display: flex; flex-direction: column; align-items: center; background: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 10px; box-shadow: 5px 5px 15px rgba(0,0,0,0.2); }
        textarea, input, button { margin: 10px; padding: 10px; width: 80%; max-width: 500px; border-radius: 5px; border: none; }
        button { background:rgb(243, 241, 133); color: Black; cursor: not-allowed; transition: transform 0.4s ease-in-out; }
        button:hover { transform: scale(1.1); background:rgb(235, 84, 84); }
        table { width: 90%; margin: 20px auto; border-collapse: collapse; background: white; }
        th, td { border: 1px solid #000; padding: 8px; text-align: center; }
        th { background-color: #007bff; color: white; }
        .download { margin-top: 20px; }
        .download a { background: green; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; transition: transform 0.2s ease-in-out; }
        .download a:hover { transform: scale(1.1); }
    </style>
</head>
<body>
    <h2>🚀 ERROR CODE WISE COUNT 🚀 </h2>
    <form method="POST">
        <label>🤖Select Date:</label>
        <input type="date" name="date" required>
        
        <label>172.17.208.123</label>
        <textarea name="input123" rows="4"></textarea>
        
        <label>172.17.208.126</label>
        <textarea name="input126" rows="4"></textarea>
        
        <label>172.17.208.243</label>
        <textarea name="input243" rows="4"></textarea>
        
        <label>172.17.208.244</label>
        <textarea name="input244" rows="4"></textarea>
        
        <label>172.17.208.120</label>
        <textarea name="input120" rows="4"></textarea>
        
        <button type="submit">🚀 Click but slowly 🚀</button>
    </form>

    {% if tables %}
        <h2>Check Excel files👀</h2>
        {% for table in tables %}
            {{ table|safe }}
        {% endfor %}
        <div class="download">
            <a href="/download">⬇ DOWNLOAD TOTAL COUNT FILE 📂</a>
        </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    data_frames = []
    selected_date = ""
    all_categories = set()

    if request.method == "POST":
        selected_date = request.form.get("date")
        input_dict = {
            "123": request.form.get("input123"),
            "126": request.form.get("input126"),
            "243": request.form.get("input243"),
            "244": request.form.get("input244"),
            "120": request.form.get("input120"),
        }
        
        for key, raw_data in input_dict.items():
            if raw_data:
                df, categories = process_input(raw_data, selected_date, key)
                data_frames.append(df)
                all_categories.update(categories)

        if data_frames:
            final_df = merge_data_frames(data_frames, all_categories)
            save_to_excel(final_df)
            return render_template_string(HTML_TEMPLATE, date=selected_date, tables=[final_df.to_html(index=False, classes='table table-bordered')])

    return render_template_string(HTML_TEMPLATE, date=selected_date, tables=[])

def process_input(raw_data, date, source):
    rows = raw_data.strip().split("\n")
    data_dict = {"Date": [date], "Source": [source]}
    categories_set = set()
    
    for row in rows:
        parts = row.strip().split()
        if len(parts) >= 2:
            try:
                value = int(float(parts[0]))
                category = parts[1].replace("|", "_")
                data_dict[category] = [value]
                categories_set.add(category)
            except ValueError:
                continue
    
    return pd.DataFrame(data_dict), categories_set

def merge_data_frames(df_list, all_categories):
    final_df = pd.DataFrame(columns=["Date", "Source"] + sorted(all_categories))
    for df in df_list:
        for category in sorted(all_categories):
            if category not in df.columns:
                df[category] = 0
        final_df = pd.concat([final_df, df], ignore_index=True)
    
    total_row = final_df.iloc[:, 2:].sum().to_frame().T
    total_row.insert(0, "Source", "Total")
    total_row.insert(0, "Date", "Total")
    final_df = pd.concat([final_df, total_row], ignore_index=True)
    return final_df

def save_to_excel(df):
    EXCEL_PATH = r"C:\Users\Harshit\OneDrive - Teledgers Technology Private Limited\Desktop\Daily_errorcodewise_count"
    os.makedirs(EXCEL_PATH, exist_ok=True)
    for source in df["Source"].unique():
        source_df = df[df["Source"] == source]
        file_path = os.path.join(EXCEL_PATH, f"{source}.xlsx")
        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            existing_df = pd.concat([existing_df, source_df], ignore_index=True)
            existing_df.to_excel(file_path, index=False)
        else:
            source_df.to_excel(file_path, index=False, engine='xlsxwriter')

@app.route("/download")
def download_file():
    EXCEL_PATH = r"C:\Users\Harshit\OneDrive - Teledgers Technology Private Limited\Desktop"
    file_path = os.path.join(EXCEL_PATH, "Total.xlsx")
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
