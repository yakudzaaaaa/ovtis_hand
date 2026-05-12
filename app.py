import os
import json
from flask import Flask, jsonify, render_template_string, request, redirect

app = Flask(__name__)
STATUS_FILE = "status.json"

def get_status():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("state", "OFF")
        except Exception:
            return "OFF"
    return "OFF"

def save_status(state):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump({"state": state}, f, ensure_ascii=False)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Status: {{ status }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background: #f5f5f5;
        }
        .status {
            font-size: 48px;
            font-weight: bold;
            margin: 20px;
        }
        .on { color: green; }
        .off { color: red; }
        button {
            padding: 15px 30px;
            font-size: 18px;
            cursor: pointer;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
        }
        button:hover { background: #0056b3; }
        .info {
            margin-top: 30px;
            padding: 15px;
            background: white;
            border-radius: 5px;
            text-align: left;
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
        }
        .url-box {
            background: #e9ecef;
            padding: 8px 12px;
            border-radius: 3px;
            font-family: monospace;
            font-size: 14px;
            word-break: break-all;
            margin: 8px 0;
            display: block;
            cursor: pointer;
        }
        .url-box:hover {
            background: #dee2e6;
        }
        .hint {
            color: #6c757d;
            font-size: 12px;
            margin-top: 2px;
        }
    </style>
</head>
<body>
    <h1>Панель управления</h1>
    <div class="status {{ status_class }}">{{ status }}</div>
    
    <form method="POST" action="/toggle">
        <button type="submit">Переключить</button>
    </form>
    
    <div class="info">
        <h3>Управление (скопируйте в адресную строку):</h3>
        
        <div class="url-box" onclick="copyToClipboard(this)">
            {{ url_root }}?status=on
            <div class="hint">← нажмите, чтобы скопировать</div>
        </div>
        
        <div class="url-box" onclick="copyToClipboard(this)">
            {{ url_root }}?status=off
            <div class="hint">← нажмите, чтобы скопировать</div>
        </div>
    </div>
    
    <script>
        function copyToClipboard(element) {
            const url = element.childNodes[0].textContent.trim();
            navigator.clipboard.writeText(url).then(function() {
                const original = element.innerHTML;
                element.innerHTML = '<span style="color: green; font-weight: bold;">✓ Скопировано!</span>';
                setTimeout(function() {
                    element.innerHTML = original;
                }, 1500);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    new_status = request.args.get('status', '').strip().upper()
    if new_status in ('ON', 'OFF'):
        save_status(new_status)
    status = get_status()
    status_class = "on" if status == "ON" else "off"
    url_root = request.url_root
    return render_template_string(HTML, status=status, status_class=status_class, url_root=url_root)

@app.route('/status')
def get_status_api():
    return jsonify({"state": get_status()})

@app.route('/toggle', methods=['POST'])
def toggle_status():
    current = get_status()
    new_state = "ON" if current == "OFF" else "OFF"
    save_status(new_state)
    return redirect('/')

if __name__ == '__main__':
    if not os.path.exists(STATUS_FILE):
        save_status("OFF")
    print(f"🌐 Сайт доступен: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)