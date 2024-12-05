from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    logger.info("Rota HOME acessada")
    return jsonify({"status": "online"})

@app.route('/search', methods=['POST'])
def search():
    logger.info(f"Recebendo requisição POST /search")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"Body: {request.get_data(as_text=True)}")
    
    data = request.json
    logger.info(f"Data parsed: {data}")
    
    query = data.get('query')
    if not query:
        logger.error("Query não fornecida")
        return jsonify({"error": "Query não fornecida"}), 400

    logger.info(f"Realizando pesquisa para query: {query}")
    result = search_google(query)
    logger.info(f"Resultado obtido: {result}")
    
    return jsonify({"result": result})

def search_google(query):
    GOOGLE_API_KEY = "AIzaSyAKaPAmMNTzIwWMPHCpKs_LtWHHN4vSNyE"
    SEARCH_ENGINE_ID = "15994e045ec3b4bee"
    
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&num=5"
    logger.info(f"URL Google Search: {url}")
    
    try:
        logger.info("Fazendo requisição para Google Search API")
        response = requests.get(url)
        response.raise_for_status()
        results = response.json()
        
        if "items" in results:
            logger.info(f"Número de resultados encontrados: {len(results['items'])}")
            search_results = [item.get('snippet', '') for item in results['items'][:5]]
            combined_results = " | ".join(search_results)
            logger.info(f"Resultados combinados: {combined_results[:100]}...")
            return combined_results
        else:
            logger.warning("Nenhum resultado encontrado na pesquisa")
            return "Nenhum resultado encontrado."
    
    except Exception as e:
        logger.error(f"Erro durante a pesquisa: {str(e)}")
        return f"Erro na pesquisa: {str(e)}"

if __name__ == '__main__':
    port = os.getenv('PORT', 8080)
    logger.info(f"Iniciando aplicação na porta {port}")
    app.run(host='0.0.0.0', port=port)
