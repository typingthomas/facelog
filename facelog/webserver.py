import os
from flask import Flask, render_template_string, send_from_directory
import socket
import logging
from . import pathmake
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Recent Detection</title>
    <meta http-equiv="refresh" content="5">
    <style>
        img {
            max-width: 90%;
            max-height: 80vh;
            border: 5px solid {{ border_color }};
        }
    </style>
</head>
<body>
    <h1>Recent Detection</h1>
    {% if latest_image %}
        <p>{{ latest_image_name }}</p>
        <img src="{{ latest_image }}" alt="{{ latest_image_name }}">
    {% else %}
        <p>No detections yet.</p>
    {% endif %}
</body>
</html>
"""

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unable to detect"

def start_webserver(host="0.0.0.0", port=5000):
    app = Flask(__name__)
    DETECTION_FOLDER = pathmake.capturepath
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.logger.disabled = True
    @app.route("/")
    def index():
        if not os.path.exists(DETECTION_FOLDER):
            os.makedirs(DETECTION_FOLDER)

        files = [f for f in os.listdir(DETECTION_FOLDER) if f.lower().endswith(".jpg")]

        if files:
            def extract_frame_count(f):
                try:
                    return int(f.split("-")[1])
                except:
                    return -1

            latest_file = max(files, key=extract_frame_count)
            border_color = "red" if "Unknown" in latest_file else "green"

            return render_template_string(
                HTML_TEMPLATE,
                latest_image=f"/image/{latest_file}",
                latest_image_name=latest_file,
                border_color=border_color
            )

        return render_template_string(
            HTML_TEMPLATE,
            latest_image=None,
            latest_image_name=None,
            border_color="green"
        )

    @app.route("/image/<filename>")
    def serve_image(filename):
        return send_from_directory(DETECTION_FOLDER, filename)

    local_ip = get_local_ip()
    print("\nfacelog Web UI is running.")
    print(f"Access locally:  http://127.0.0.1:{port}")
    print(f"Access on network: http://{local_ip}:{port}\n")
    
    app.run(
        host=host,
        port=port,
        debug=False,
        use_reloader=False
    )
