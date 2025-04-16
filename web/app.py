from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Конфигурация (можно вынести в .env)
app.config['BOT_API_URL'] = 'http://bot:8000'

@app.get('/')
def control_panel():
    """Главная страница с кнопками управления"""
    return render_template('control.html')

@app.post('/api/bot/start')
def start_bot():
    """Запуск бота через API"""
    try:
        response = requests.post(
            f"{app.config['BOT_API_URL']}/start",
            timeout=5
        )
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.post('/api/bot/stop')
def stop_bot():
    """Остановка бота через API"""
    try:
        response = requests.post(
            f"{app.config['BOT_API_URL']}/stop",
            timeout=5
        )
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.post('/api/bot/check')
def status_bot():
    """Статус бота через API"""
    try:
        response = requests.post(
            f"{app.config['BOT_API_URL']}/check",
            timeout=5
        )
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)