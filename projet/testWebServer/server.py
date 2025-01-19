from flask import Flask, render_template_string, request
import subprocess

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exécuter Scripts et Flux MJPEG</title>
</head>
<body>
    <h1>Exécuter un script</h1>
    <form method="post">
        <label for="script_choice">Choisir un script :</label>
        <select name="script_choice" id="script_choice">
            <option value="script-1">Script 1</option>
            <option value="script-2">Script 2</option>
        </select>
        <button type="submit">Exécuter le script</button>
    </form>
    
    {% if output %}
        <h2>Sortie du script :</h2>
        <pre>{{ output }}</pre>
    {% endif %}
    
    <h1>Flux MJPEG</h1>
    <img src="http://192.168.1.22:5050" alt="Flux vidéo" style="width: 100%; max-width: 640px; height: auto; border: 1px solid #ccc;">
</body>
</html>
"""

# Mise à jour de la route pour gérer deux scripts différents
@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    script_path = None
    
    if request.method == "POST":
        script_choice = request.form.get("script_choice")
        
        # Choisir le script à exécuter en fonction de l'option sélectionnée
        if script_choice == "script-1":
            script_path = "/home/pi/Git/hailo-rpi5-examples/projet/testWebServer/lancer-ia"
        elif script_choice == "script-2":
            script_path = "/home/pi/Git/hailo-rpi-examples/projet/testWebServer/afficher-resultats.sh"
        
        if script_path:
            try:
                # Exécuter le script choisi
                result = subprocess.run(
                    ["/bin/bash", script_path], capture_output=True, text=True, check=True
                )
                if script_choice == "script-1":
                    output = "l'IA est en train de tourner"
                else:
                    output = result.stdout  # Capture stdout
            except subprocess.CalledProcessError as e:
                output = f"Erreur lors de l'exécution du script : {e.stderr}"
    
    return render_template_string(HTML_TEMPLATE, output=output)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
