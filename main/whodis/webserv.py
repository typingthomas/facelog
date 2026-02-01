# recent_detection_server.py
# recent_detection_server.py
import os
from datetime import datetime
import pathmake
from flask import Flask, render_template_string, send_from_directory
app = Flask(__name__)
DETECTION_FOLDER = pathmake.capturepath  # folder where detection images are stored


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

@app.route("/")

def index():
    if not os.path.exists(DETECTION_FOLDER):
        os.makedirs(DETECTION_FOLDER)

    files = [f for f in os.listdir(DETECTION_FOLDER) if f.lower().endswith(".jpg")]

    if files:
        def extract_frame_count(f):
            try:
                parts = f.split("-")
                return int(parts[1])
            except:
                return -1

        latest_file = max(files, key=extract_frame_count)

        # Decide border color
        border_color = "red" if "Unknown" in latest_file else "green"

        return render_template_string(
            HTML_TEMPLATE,
            latest_image=f"/image/{latest_file}",
            latest_image_name=latest_file,
            border_color=border_color
        )
    else:
        return render_template_string(
            HTML_TEMPLATE,
            latest_image=None,
            latest_image_name=None,
            border_color="green"
        )
    
@app.route("/image/<filename>")
def serve_image(filename):
    return send_from_directory(DETECTION_FOLDER, filename)

if __name__ == "__main__":
    if not os.path.exists(DETECTION_FOLDER):
        os.makedirs(DETECTION_FOLDER)
    app.run(host="0.0.0.0", port=5000, debug=False)
