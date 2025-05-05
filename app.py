from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
from models.rag_service import RAGService
from models.vector_db import setup_vector_db
from models.product_catalog import load_product_catalog

load_dotenv()

app = Flask(__name__)

products = load_product_catalog()
vector_db = setup_vector_db()
rag_service = RAGService(vector_db, products)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/api/products/<int:product_id>')
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/query', methods=['POST'])
def process_query():
    data = request.json
    query = data.get('query', '')
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    
    result = rag_service.process_query(query)
    return jsonify(result)

@app.route('/api/query/followup', methods=['POST'])
def process_followup_query():
    data = request.json
    original_query = data.get('originalQuery', '')
    followup_query = data.get('followupQuery', '')
    
    if not original_query or not followup_query:
        return jsonify({"error": "Missing query parameters"}), 400
    
    result = rag_service.process_followup_query(original_query, followup_query)
    return jsonify(result)

@app.route('/api/model-info')
def get_model_info():
    info = rag_service.get_model_info()
    return jsonify(info)

@app.route('/api/technical-info')
def get_technical_info():
    info = rag_service.get_technical_info()
    return jsonify(info)

@app.route('/api/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({
            "error": "Missing query parameter",
            "usage": "Use ?q=your search query"
        }), 400
    
    result = rag_service.process_query(query, max_results=10, threshold=0.3)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)