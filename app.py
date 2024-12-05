from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "online"})

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "Query não fornecida"}), 400
    
    result = search_google(query)
    return jsonify({"result": result})

def search_google(query):
    GOOGLE_API_KEY = "AIzaSyAKaPAmMNTzIwWMPHCpKs_LtWHHN4vSNyE"
    SEARCH_ENGINE_ID = "15994e045ec3b4bee"
    
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&num=5"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json()
        
        if "items" in results:
            search_results = [item.get('snippet', '') for item in results['items'][:5]]
            combined_results = " | ".join(search_results)
            return combined_results
        else:
            return "Nenhum resultado encontrado."
    
    except Exception as e:
        return f"Erro na pesquisa: {str(e)}"

if __name__ == '__main__':
    port = os.getenv('PORT', 8080)
    app.run(host='0.0.0.0', port=port)

