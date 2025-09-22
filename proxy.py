from flask import Flask, request, send_file
from flask_cors import CORS
import requests
from io import BytesIO

app = Flask(__name__)
CORS(app) # Abilita CORS per tutte le rotte

@app.route('/proxy')
def proxy_image():
    image_url = request.args.get('url')
    if not image_url:
        return "URL mancante", 400

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(image_url, stream=True, headers=headers)
        response.raise_for_status()

        return send_file(
            BytesIO(response.content),
            mimetype=response.headers.get('Content-Type')
        )
    except requests.exceptions.RequestException as e:
        return f"Errore nel recuperare l'immagine: {e}", 500

if __name__ == '__main__':
    app.run(port=5000)
