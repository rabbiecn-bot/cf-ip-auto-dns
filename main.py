import os
import re
import requests
from bs4 import BeautifulSoup

# =========================
# 配置
# =========================

SOURCE_URL = "https://api.uouin.com/cloudflare.html"

DNSHE_API = (
    "https://api005.dnshe.com/index.php"
    "?m=domain_hub"
    "&endpoint=dns_records"
)

API_KEY = os.environ["DNSHE_KEY"]
API_SECRET = os.environ["DNSHE_SECRET"]

SUBDOMAIN_ID = 7007606429

DNS_RECORDS = {
    "电信": {
        "id": 617167586773195,
        "name": "ct"
    },
    "联通": {
        "id": 550278722553804,
        "name": "cu"
    },
    "移动": {
        "id": 662403211220243,
        "name": "cm"
    }
}


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 "
        "(KHTML, like Gecko)"
        " Chrome/138 Safari/537.36"
    )
}


# =========================
# 下载网页
# =========================

def fetch_html():

    print("开始获取网页...")

    r = requests.get(
        SOURCE_URL,
        headers=HEADERS,
        timeout=20
    )

    r.raise_for_status()

    print("网页获取成功")
    

    return r.text
