@app.route('/search', methods=['POST'])
def search():
    print("Recebendo requisição:", request.json)  # Log da requisição
    data = request.json
    query = data.get('query')
    if not query:
        print("Query não fornecida")  # Log de erro
        return jsonify({"error": "Query não fornecida"}), 400
    
    print(f"Pesquisando por: {query}")  # Log da query
    result = search_google(query)
    print(f"Resultado: {result}")  # Log do resultado
    return jsonify({"result": result})
