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
    <title>File Content Viewer</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <script>
        async function fetchContent() {
            try {
                const response = await fetch('/content');
                const data = await response.json();

                const contentContainer = document.getElementById('content');
                contentContainer.innerHTML = ''; // Clear current content

                // Add each line from the file
                data.forEach(line => {
                    const li = document.createElement('li');
                    li.textContent = line.trim();
                    contentContainer.appendChild(li);
                });
            } catch (error) {
                console.error('Error fetching content:', error);
            }
        }

        // Fetch content every second
        setInterval(fetchContent, 1000);

        // Fetch content on initial page load
        window.onload = fetchContent;
    </script>
</head>
<nav>
    <img src ="{{ url_for('static', filename='logo.png') }}" alt="logo projet">
</nav>
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
                    <button type="submit" name="script_choice" value="script-1">Lance l'IA</button>
                </form>
                <form method="post">
                    <button type="submit" name="script_choice" value="script-2">Clean</button>
                </form>
            </div>
        </div>
    </div>
    <ul id="content">
        <!-- Content will be dynamically added here -->
    </ul>
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
