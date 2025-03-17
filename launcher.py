from flask import Flask, render_template_string, redirect, url_for
import subprocess
import os
import psutil
import time

app = Flask(__name__)


projects = {
    "server-wise-count": "C:\\Users\\Harshit\\OneDrive - Teledgers Technology Private Limited\Desktop\\new py codes\\python 3 main py codes\\SERVER WISE COUNT.py",
    "total-error-code-wise-count": "C:\\Users\\Harshit\\OneDrive - Teledgers Technology Private Limited\Desktop\\new py codes\\python 3 main py codes\\TOTAL ERROR CODE WISE COUNT.py",
    "logs-to-xml": "C:\\Users\\Harshit\\OneDrive - Teledgers Technology Private Limited\Desktop\\new py codes\\python 3 main py codes\\LOGS to XML.py",
    "epoch-convertor": "C:\\Users\\Harshit\\OneDrive - Teledgers Technology Private Limited\Desktop\\new py codes\\python 3 main py codes\\Test.py",
    "Excel-process": "C:\\Users\\Harshit\\OneDrive - Teledgers Technology Private Limited\Desktop\\new py codes\\python 3 main py codes\\excel_proess.py"
}

project_ports = {
    "server-wise-count": 5001,
    "total-error-code-wise-count": 5002,
    "logs-to-xml": 5003,
    "epoch-convertor": 5004,
    "Excel-process": 5005
}

LOGO_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRQ0HqT9dk3DeLLbBHebie1wSK7HYWCudOCw&s"
INSTAGRAM_URL = "https://instagram.com/harshit__2244"
EMAIL = "mailto:harshitsharma31152@gmail.com"
PHONE = "tel:+918219673715"

def is_port_in_use(port):
    """Check if a port is already in use."""
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            return True
    return False

@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Project Launcher</title>
        <link rel="icon" type="image/png" href="{{ logo_url }}">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
        <style>
            body {
                background: linear-gradient(45deg, #101010, #1a1a1a, #222222);
                color: #fff;
                font-family: 'Poppins', sans-serif;
                text-align: center;
                padding-top: 30px;
            }
            .container {
                max-width: 800px;
                margin: auto;
                padding: 20px;
            }
            h1 {
                font-size: 1.8em;
                text-shadow: 0px 0px 10px cyan;
                margin-bottom: 30px;
            }
            .logo-container img {
                width: 130px;
                height: 130px;
                border-radius: 50%;
                box-shadow: 0 0 15px cyan;
                margin-bottom: 20px;
            }
            .projects {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .project-btn {
                width: 75%;
                padding: 14px;
                margin: 12px 0;
                border-radius: 15px;
                text-decoration: none;
                font-size: 1.2em;
                font-weight: bold;
                background: linear-gradient(90deg, #00ffcc, #0099ff);
                color: black;
                transition: 0.3s;
                box-shadow: 0 0 18px cyan;
            }
            .project-btn:hover {
                transform: scale(1.12);
                box-shadow: 0 0 22px cyan;
            }
            .social-icons {
                margin-top: 50px;
            }
            .social-icons a {
                color: cyan;
                font-size: 2em;
                margin: 20px;
                transition: 0.3s;
                text-decoration: none;
            }
            .social-icons a:hover {
                color: #00ffcc;
                transform: scale(1.3);
            }
            .footer {
                margin-top: 50px;
                background: rgba(0, 0, 0, 0.8);
                padding: 20px 0;
                text-align: center;
                font-size: 1em;
                color: cyan;
                box-shadow: 0 0 15px cyan;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo-container">
                <img src="{{ logo_url }}" alt="Project Launcher Logo">
            </div>
            <h1>🚀 Choose a Project to Launch</h1>
            <div class="projects">
                {% for name, path in projects.items() %}
                    <a href="{{ url_for('launch_project', project_name=name) }}" class="project-btn">{{ name.replace('-', ' ').upper() }}</a>
                {% endfor %}
            </div>
            <div class="social-icons">
                <a href="{{ instagram_url }}" target="_blank"><i class="fa-brands fa-instagram"></i></a>
                <a href="{{ email }}"><i class="fa-solid fa-envelope"></i></a>
                <a href="{{ phone }}"><i class="fa-solid fa-phone"></i></a>
            </div>
        </div>
        <div class="footer">© Copyright Harshit Sharma</div>
    </body>
    </html>
    """, projects=projects, logo_url=LOGO_URL, instagram_url=INSTAGRAM_URL, email=EMAIL, phone=PHONE)

@app.route("/launch/<project_name>")
def launch_project(project_name):
    """Launch a project if it's not already running."""
    project_name = project_name.lower()
    
    if project_name in projects:
        project_path = projects[project_name]
        project_port = project_ports[project_name]

        if is_port_in_use(project_port):
            return redirect(f"http://127.0.0.1:{project_port}")

        process = subprocess.Popen(
            ["python", project_path, "--host=127.0.0.1", "--port=" + str(project_port)], 
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        time.sleep(3)
        return redirect(f"http://127.0.0.1:{project_port}")
    
    return "Project not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
