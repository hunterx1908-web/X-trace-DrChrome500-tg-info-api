import os
import requests
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 🔑 Teri API Key
VALID_KEY = "@x_TRACEOWNER"

# 🔥 Cloudflare Worker Proxy URL
PROXY_URL = os.environ.get('PROXY_URL', 'https://tg-info-proxy.YOUR_USERNAME.workers.dev')

# 🔥 API Expiry Date
API_EXPIRY = "2026-12-31"

def is_expired():
    try:
        expiry = datetime.strptime(API_EXPIRY, "%Y-%m-%d")
        return datetime.utcnow() > expiry
    except:
        return False

@app.route('/')
def home():
    return jsonify({
        "status": True,
        "message": "TG Info API is working! (X-TRACE Edition)",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER",
        "expires_on": API_EXPIRY,
        "status": "Active" if not is_expired() else "Expired",
        "endpoints": {
            "info": "/api?key=YOUR_KEY&type=uers&term=TG_ID_OR_USERNAME"
        },
        "example": "/api?key=@x_TRACEOWNER&type=uers&term=8328548512"
    })

@app.route('/api')
def tg_info():
    if is_expired():
        return jsonify({
            "status": False,
            "error": f"API expired on {API_EXPIRY}!",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER",
            "expires_on": API_EXPIRY
        }), 401
    
    key = request.args.get('key')
    term = request.args.get('term')
    query_type = request.args.get('type', 'uers')
    
    if not key:
        return jsonify({"status": False, "error": "Missing API Key!", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 400
        
    if key != VALID_KEY:
        return jsonify({"status": False, "error": "Invalid API Key!", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 401
    
    if not term:
        return jsonify({"status": False, "error": "Missing 'term' parameter!", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 400
    
    try:
        response = requests.get(PROXY_URL, params={
            'key': 'jsjdne',
            'type': query_type,
            'term': term
        }, timeout=15)
        
        response.raise_for_status()
        data = response.json()
        
        # 🔥 Clean response
        if isinstance(data, dict):
            data.pop('developer', None)
            data.pop('key_details', None)
            data.pop('status_code', None)
            data.pop('http_status', None)
            
            if data.get('success') == True and data.get('number'):
                data['developer'] = '@x_TRACEOWNER'
                data['credit'] = '@x_TRACEOWNER'
                data['api_expires_on'] = API_EXPIRY
                return jsonify(data)
            else:
                return jsonify({
                    "status": False,
                    "message": "Phone number not found",
                    "developer": "@x_TRACEOWNER",
                    "credit": "@x_TRACEOWNER"
                }), 404
        
        return jsonify(data)
        
    except requests.exceptions.Timeout:
        return jsonify({"status": False, "message": "Request timeout. Please try again later.", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 504
        
    except Exception as e:
        return jsonify({"status": False, "message": "No data found", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 404

@app.route('/api/<path:path>')
def catch_all(path):
    return jsonify({"status": False, "message": "No data found", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": False, "message": "No data found", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": False, "message": "No data found", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))