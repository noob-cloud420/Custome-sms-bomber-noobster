import time

def fetch_devices(config):
    """Fetch devices with timeout and retry"""
    url = f"{config['url']}/clients.json?auth={config['auth']}"
    
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data:
                    devices = []
                    for client_id, info in data.items():
                        # ONLINE CHECK
                        is_online = info.get('status') == True or safe_int(info.get('battery')) > 0
                        if is_online:
                            devices.append({
                                "id": client_id,
                                "battery": info.get('battery', 'N/A'),
                                "is_online": True,
                                "firebase": config['name'],
                                "config": config
                            })
                    return devices
            time.sleep(1)
        except:
            time.sleep(2)
    return []
