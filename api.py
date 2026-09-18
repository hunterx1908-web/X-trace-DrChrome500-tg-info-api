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

# 🔥 API Expiry Date (Apni marzi se change kar)
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
    # 🔥 Check if API is expired
    if is_expired():
        return jsonify({
            "status": False,
            "error": f"API expired on {API_EXPIRY}! Please contact support.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER",
            "expires_on": API_EXPIRY
        }), 401
    
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
    
    params = {'key': ORIGINAL_KEY, 'type': query_type, 'term': term}
    
    try:
        response = requests.get(ORIGINAL_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # 🔥 Clean response
        if isinstance(data, dict):
            # Remove unwanted fields
            data.pop('developer', None)
            data.pop('key_details', None)
            data.pop('status_code', None)
            data.pop('http_status', None)
            
            # 🔥 FIX: Check if success hai aur number hai
            if data.get('success') == True and data.get('number'):
                # Data mil gaya — clean response
                data['developer'] = '@x_TRACEOWNER'
                data['credit'] = '@x_TRACEOWNER'
                data['api_expires_on'] = API_EXPIRY
                return jsonify(data)
            else:
                # Data nahi mila
                return jsonify({
                    "status": False,
                    "message": "Phone number not found",
                    "developer": "@x_TRACEOWNER",
                    "credit": "@x_TRACEOWNER"
                }), 404
            
        return jsonify(data)
        
    except requests.exceptions.Timeout:
        return jsonify({"status": False, "message": "Request timeout. Please try again later.", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 504
        
    except requests.exceptions.ConnectionError:
        return jsonify({"status": False, "message": "No data found", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 404
        
    except requests.exceptions.RequestException:
        return jsonify({"status": False, "message": "No data found", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 404
        
    except Exception:
        return jsonify({"status": False, "message": "No data found", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 404

# ==================== TEST ENDPOINT ====================
@app.route('/test-original')
def test_original():
    """
    Ye endpoint original API ko direct call karta hai.
    Isse pata chalega ki:
    - Original API response de rahi hai ya nahi
    - Status code kya hai
    - Headers kya hain
    """
    term = request.args.get('term', '@Thakur_bolti_public')
    
    try:
        response = requests.get(ORIGINAL_API_URL, params={
            'key': ORIGINAL_KEY,
            'type': 'uers',
            'term': term
        }, timeout=10)
        
        return jsonify({
            "status": "success",
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "raw_response": response.text,
            "json_response": response.json() if response.text else None
        })
        
    except requests.exceptions.Timeout:
        return jsonify({
            "status": "timeout",
            "error": "Original API 10 sec mein response nahi di"
        }), 504
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            "status": "connection_error",
            "error": "Original API se connect nahi ho paya"
        }), 503
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

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