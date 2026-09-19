import os
import requests
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 🔑 Teri API Key
VALID_KEY = "@DrChrome500"

# 🔥 Cloudflare Worker URL
PROXY_URL = "https://x-trace-tg-full-info-api.hunterx1908.workers.dev/"

# 🔥 API Expiry Date
API_EXPIRY = "2026-09-22"

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
            "info": "/api?key=YOUR_KEY&type=uers&term=TG_ID"
        },
        "example": "/api?key=@DrChrome500&type=uers&term=@GURUJI_33"
    })

@app.route('/api')
def tg_info():
    # 🔥 Check if API is expired
    if is_expired():
        return jsonify({
            "status": False,
            "error": f"API expired on {API_EXPIRY}!",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER",
            "expires_on": API_EXPIRY
        }), 401
    
    # Get parameters
    key = request.args.get('key')
    term = request.args.get('term')
    query_type = request.args.get('type', 'uers')
    
    # 🔐 Key verify
    if not key:
        return jsonify({"status": False, "error": "Missing API Key!", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 400
        
    if key != VALID_KEY:
        return jsonify({"status": False, "error": "Invalid API Key!", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 401
    
    if not term:
        return jsonify({"status": False, "error": "Missing 'term' parameter!", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 400
    
    try:
        # 🔥 Cloudflare Worker ko call kar
        response = requests.get(PROXY_URL, params={
            'key': '@x_TRACEOWNER',
            'type': query_type,
            'term': term
        }, timeout=15)
        
        response.raise_for_status()
        data = response.json()
        
        # 🔥 Expiry date add kar
        if isinstance(data, dict):
            data['api_expires_on'] = API_EXPIRY
        
        return jsonify(data)
        
    except requests.exceptions.Timeout:
        return jsonify({"status": False, "message": "Request timeout. Please try again later.", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 504
        
    except requests.exceptions.ConnectionError:
        return jsonify({"status": False, "message": "Request timeout. Please try again later.", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 504
        
    except requests.exceptions.RequestException:
        return jsonify({"status": False, "message": "No data found", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 404
        
    except Exception:
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