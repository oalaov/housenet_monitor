from flask import Flask, jsonify, render_template_string
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Traffic Monitor</title>
    <style>
        body { font-family: monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; }
        h1 { color: #4ec9b0; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { text-align: left; padding: 10px; background: #333; }
        td { padding: 8px; border-bottom: 1px solid #333; }
        .TCP { color: #4ec9b0; }
        .UDP { color: #ce9178; }
        .OTHER { color: #888; }
        .time { color: #888; }
    </style>
</head>
<body>
    <h1>📡 Traffic Monitor</h1>
    <p>Обновляется каждые 3 секунды</p>
    <table>
        <thead>
            <tr>
                <th>Время</th>
                <th>Протокол</th>
                <th>Откуда</th>
                <th>Порт</th>
                <th>Куда</th>
                <th>Порт</th>
                <th>Размер (байт)</th>
            </tr>
        </thead>
        <tbody id="data"></tbody>
    </table>

    <script>
        function loadData() {
            fetch('/api/traffic')
                .then(response => response.json())
                .then(data => {
                    const tbody = document.getElementById('data');
                    tbody.innerHTML = data.map(p => `
                        <tr>
                            <td class="time">${new Date(p.time * 1000).toLocaleTimeString()}</td>
                            <td class="${p.proto}">${p.proto}</td>
                            <td>${p.src}</td>
                            <td>${p.sport}</td>
                            <td>${p.dst}</td>
                            <td>${p.dport}</td>
                            <td>${p.size}</td>
                        </tr>
                    `).join('');
                })
                .catch(error => console.error('Ошибка загрузки:', error));
        }

        // Загружаем сразу
        loadData();
        
        // И каждые 3 секунды
        setInterval(loadData, 3000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/traffic')
def get_traffic():
    try:
        with open('traffic_data.json', 'r') as f:
            data = json.load(f)
        return jsonify(data[-50:])
    except:
        return jsonify([])

if __name__ == '__main__':
    print("=== FLASK SERVER ===")
    print("Открой браузер: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)