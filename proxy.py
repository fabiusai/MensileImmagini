from flask import Flask, request, send_file
from flask_cors import CORS  # Importa la libreria CORS
import requests
from io import BytesIO

app = Flask(__name__)

# Questa riga è la soluzione: permette al frontend di comunicare col backend
CORS(app)

@app.route('/proxy')
def proxy_image():
    image_url = request.args.get('url')
    if not image_url:
        return "URL mancante", 400

    try:
        # Aggiungiamo un User-Agent per far finta di essere un browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(image_url, stream=True, headers=headers)
        response.raise_for_status()

        return send_file(
            BytesIO(response.content),
            mimetype=response.headers.get('Content-Type')
        )
    except requests.exceptions.RequestException as e:
        return f"Errore nel recuperare l'immagine: {e}", 500

# Aggiungiamo una rotta base per confermare che il server è attivo
@app.route('/')
def home():
    return "Proxy server is running!"

if __name__ == '__main__':
    app.run(port=5000)
