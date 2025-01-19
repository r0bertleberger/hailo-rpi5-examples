from flask import Flask, render_template_string, request
import subprocess

app = Flask(__name__)

SCRIPT_PATH = "test.sh"

# La page WEB execute le script `test.sh` et affiche directement le flux MJPEG (depuis l'ESP32) donc pas utilisable
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exécuter Hello World et Flux MJPEG</title>
</head>
<body>
    <h1>Exécuter le script Python</h1>
    <form method="post">
        <button type="submit">Exécuter le script</button>
    </form>
    {% if output %}
        <h2>Sortie du script :</h2>
        <pre>{{ output }}</pre>
    {% endif %}
    <h1>Flux MJPEG</h1>
    <img src="http://192.168.1.3:81/stream" alt="Flux vidéo" style="width: 100%; max-width: 640px; height: auto; border: 1px solid #ccc;">
</body>
</html>
"""
@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    if request.method == "POST":
        try:
            # Run the Bash script
            result = subprocess.run(
                ["/bin/bash", SCRIPT_PATH], capture_output=True, text=True, check=True
            )
            output = result.stdout  # Capture stdout
        except subprocess.CalledProcessError as e:
            output = f"Error while executing the script: {e.stderr}"

    return render_template_string(HTML_TEMPLATE, output=output)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
