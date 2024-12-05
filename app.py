from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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
            # Coleta os snippets dos primeiros 5 resultados
            search_results = [item.get('snippet', '') for item in results['items'][:5]]
            # Junta todos os resultados em um único texto
            combined_results = " | ".join(search_results)
            return combined_results
        else:
            return "Nenhum resultado encontrado."
    
    except Exception as e:
        return f"Erro na pesquisa: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


