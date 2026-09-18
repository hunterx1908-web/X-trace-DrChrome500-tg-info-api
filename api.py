import os
import requests
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 🔑 Teri API Key
VALID_KEY = "@x_TRACEOWNER"

# Original API details
ORIGINAL_API_URL = "http://uersxinfo.in/api"
ORIGINAL_KEY = "jsjdne"

# 🔥 Free Proxy URLs (multiple fallback)
PROXY_URLS = [
    "https://api.allorigins.win/raw?url=",
    "https://corsproxy.io/?",
    "https://api.codetabs.com/v1/proxy?quest=",
]

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
            "info": "/api?key=YOUR_KEY&type=uers&term=TG_ID_OR_USERNAME",
            "test": "/test-original?term=TG_ID_OR_USERNAME"
        },
        "example": "/api?key=@x_TRACEOWNER&type=uers&term=8328548512"
    })

# ==================== MAIN API ====================
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
    
    # 🔥 Original API URL with parameters
    original_url = f"{ORIGINAL_API_URL}?key={ORIGINAL_KEY}&type={query_type}&term={term}"
    
    data = None
    last_error = None
    
    # 🔥 Try direct first
    try:
        response = requests.get(original_url, timeout=10)
        if response.status_code == 200 and response.text:
            data = response.json()
    except:
        pass
    
    # 🔥 If direct fails, try proxies
    if not data:
        for proxy in PROXY_URLS:
            try:
                proxy_url = proxy + original_url if '?' in proxy else proxy + original_url
                response = requests.get(proxy_url, timeout=15)
                if response.status_code == 200 and response.text:
                    data = response.json()
                    if data:
                        break
            except:
                continue
    
    # 🔥 If still no data
    if not data:
        return jsonify({
            "status": False,
            "message": "Request timeout. Please try again later.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 504
    
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

# ==================== TEST ENDPOINT ====================
@app.route('/test-original')
def test_original():
    term = request.args.get('term', '@Thakur_bolti_public')
    original_url = f"{ORIGINAL_API_URL}?key={ORIGINAL_KEY}&type=uers&term={term}"
    
    results = {}
    
    # Test direct
    try:
        r = requests.get(original_url, timeout=10)
        results['direct'] = {
            "status_code": r.status_code,
            "response": r.text[:300]
        }
    except Exception as e:
        results['direct'] = {"error": str(e)}
    
    # Test proxies
    for i, proxy in enumerate(PROXY_URLS):
        try:
            proxy_url = proxy + original_url
            r = requests.get(proxy_url, timeout=15)
            results[f'proxy_{i+1}'] = {
                "proxy": proxy,
                "status_code": r.status_code,
                "response": r.text[:300]
            }
        except Exception as e:
            results[f'proxy_{i+1}'] = {"proxy": proxy, "error": str(e)}
    
    return jsonify(results)

# ==================== ERROR HANDLERS ====================
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