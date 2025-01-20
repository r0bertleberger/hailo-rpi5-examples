from flask import Flask, render_template_string, request, Response
import subprocess
import requests

app = Flask(__name__)

# partie HTML / appel du CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exécuter Scripts et Flux MJPEG</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        <!-- Vidéo -->
        <div class="video-container">
            <h1>Flux MJPEG</h1>
            <img src="/video_feed" alt="Flux vidéo">
        </div>

        <!-- Scripts -->
        <div class="script-container">
            <h1>Exécuter un script</h1>
            
            <!-- Boutons de sélection de scripts -->
            <div class="script-buttons">
                <form method="post">
                    <button type="submit" name="script_choice" value="script-1">Script 1</button>
                </form>
                <form method="post">
                    <button type="submit" name="script_choice" value="script-2">Script 2</button>
                </form>
            </div>

            <!-- Résultats -->
            {% if output %}
                <div class="script-output">
                    <h2>Sortie du script :</h2>
                    <pre>{{ output }}</pre>
                </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""


# choix puis exécution du script
@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    script_path = None
    
    if request.method == "POST":
        script_choice = request.form.get("script_choice")
        if script_choice == "script-1":
            script_path = "/home/r0bert/Git/hailo-rpi5-examples/projet/testWebServer/scr1.sh"
        elif script_choice == "script-2":
            script_path = "/home/r0bert/Git/hailo-rpi5-examples/projet/testWebServer/scr2.sh"
        
        if script_path:
            try:
                result = subprocess.run(
                    ["/bin/bash", script_path], capture_output=True, text=True, check=True
                )
                if script_choice == "script-1":
                    output = result.stdout
                else:
                    output = "nettoyage en cours"
            except subprocess.CalledProcessError as e:
                output = f"Erreur lors de l'exécution du script : {e.stderr}"
    
    return render_template_string(HTML_TEMPLATE, output=output)

# proxy pour la vidéo
@app.route("/video_feed")
def video_feed():
    """
    Proxy pour le flux MJPEG d'un autre serveur.
    """
    # serv loopback pcq on fait office de proxy
    mjpeg_url = "http://127.0.0.1:5050"

    def proxy_stream():
        with requests.get(mjpeg_url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk

    return Response(proxy_stream(), content_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
