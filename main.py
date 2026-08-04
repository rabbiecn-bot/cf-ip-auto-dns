import os
import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
# =========================
# 配置
# =========================

SOURCE_URL = "https://v2rayssr.com/cfip/"

DNSHE_API = (
    "https://api005.dnshe.com/index.php"
    "?m=domain_hub"
    "&endpoint=dns_records"
)

API_KEY = os.environ["DNSHE_KEY"]
API_SECRET = os.environ["DNSHE_SECRET"]
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")
TG_MESSAGE = []

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
# Telegram通知
# =========================

def send_tg():

    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        print("TG配置缺失")
        return

    message = "\n".join(TG_MESSAGE)

    print("准备发送TG:")
    print(message)

    url = (
        f"https://api.telegram.org/"
        f"bot{TG_BOT_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": TG_CHAT_ID,
        "text": message
    }

    try:

        r = requests.post(
            url,
            data=data,
            timeout=10
        )

        print("TG返回:")
        print(r.text)

    except Exception as e:

        print("TG发送失败:", e)

# =========================
# 下载网页
# =========================

def fetch_html():

    print("开始获取网页...")

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(
            SOURCE_URL,
            wait_until="networkidle",
            timeout=60000
        )

        # 等待页面JS加载完成
        page.wait_for_timeout(3000)

        html = page.content()

        browser.close()

    print("网页获取成功")

    return html
    # =========================
# 解析网页
# =========================

IP_REGEX = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)
BANDWIDTH_REGEX = re.compile(
    r"(\d+(?:\.\d+)?)mb",
    re.I
)


def parse_ip(html):

    print("开始解析网页...")

    soup = BeautifulSoup(html, "html.parser")

    result = {
        "电信": None,
        "联通": None,
        "移动": None
    }
    
    bandwidth = {
        "电信": None,
        "联通": None,
        "移动": None
    }

    tables = soup.find_all("table")

    for table in tables:

        rows = table.find_all("tr")

        for row in rows:

            text = row.get_text(" ", strip=True)

            ip_match = IP_REGEX.search(text)

            if not ip_match:
                continue

            ip = ip_match.group()
            bw_match = BANDWIDTH_REGEX.findall(text)

            if bw_match:
            
                bw = float(bw_match[-1])
            
            else:
            
                bw = 0

            if "电信" in text and result["电信"] is None:

                if bw < 100:
            
                    print(
                        f"跳过电信 {ip}，带宽 {bw}Mbps < 100Mbps"
                    )
            
                    TG_MESSAGE.append(
                        f"⚠️ 电信跳过,因带宽：{bw}Mbps<100M"
                    )
            
                    result["电信"] = "SKIP"
                else:

                    result["电信"] = ip
            
                    print(
                        f"找到电信IP：{ip} 带宽：{bw}Mbps"
                    )
            
                    TG_MESSAGE.append(
                        f"📡 电信：{ip}🚀 带宽：{bw}Mbps"
                    )
                result["电信"] = ip
                bandwidth["电信"] = bw
                print(f"找到电信IP：{ip}")


            elif "联通" in text and result["联通"] is None:

                if bw < 100:
            
                    print(
                        f"跳过联通 {ip}，带宽 {bw}Mbps < 100Mbps"
                    )
            
                    TG_MESSAGE.append(
                        f"⚠️ 联通跳过,因带宽：{bw}Mbps<100M"
                    )
            
                    result["联通"] = "SKIP"
                else:

                    result["联通"] = ip
            
                    print(
                        f"找到联通IP：{ip} 带宽：{bw}Mbps"
                    )
            
                    TG_MESSAGE.append(
                        f"📡 联通：{ip}🚀 带宽：{bw}Mbps"
                    )
            
                result["联通"] = ip
                bandwidth["联通"] = bw
                print(f"找到联通IP：{ip}")

            elif "移动" in text and result["移动"] is None:

                if bw < 100:
            
                    print(
                        f"跳过移动 {ip}，带宽 {bw}Mbps < 100Mbps"
                    )
            
                    TG_MESSAGE.append(
                        f"⚠️ 移动跳过,因带宽：{bw}Mbps<100M"
                    )
            
                    result["移动"] = "SKIP"
                else:

                    result["移动"] = ip
            
                    print(
                        f"找到移动IP：{ip} 带宽：{bw}Mbps"
                    )
            
                    TG_MESSAGE.append(
                        f"📡 移动：{ip}🚀 带宽：{bw}Mbps"
                    )

                result["移动"] = ip
                bandwidth["移动"] = bw
                print(f"找到移动IP：{ip}")

            if all(result.values()):
                break

        if all(result.values()):
            break

    missing = []
    
    for k, v in result.items():
        if v is None:
            missing.append(k)
    
    if missing:

        msg = (
            "⚠️ 未解析到："
            + ",".join(missing)
        )
    
        print(msg)
    
        TG_MESSAGE.append(msg)


    print()

    print("解析完成：")

    print(f"电信：{result['电信']}")
    print(f"联通：{result['联通']}")
    print(f"移动：{result['移动']}")

    print()

    return result
    # =========================
# 更新DNS
# =========================

def update_dns(record_info, ip):

    print(f"更新 {record_info['name']} -> {ip}")

    r = requests.post(
        DNSHE_API + "&action=modify",
        headers={
            "X-API-Key": API_KEY,
            "X-API-Secret": API_SECRET
        },
        json={
            "id": record_info["id"],
            "subdomain_id": SUBDOMAIN_ID,
            "type": "A",
            "name": record_info["name"],
            "content": ip,
            "ttl": 600
        },
        timeout=20
    )

    print("HTTP:", r.status_code)

    try:
        data = r.json()
    except Exception:
        print(r.text)
        raise

    print(data)

    if not data.get("success", False):
        raise RuntimeError(
            f"{record_info['name']} 更新失败：{data}"
        )

    print(f"{record_info['name']} 更新成功\n")

    TG_MESSAGE.append(
        f"✅ {record_info['name']} 更新成功"
    )
    
    # =========================
# 主程序
# =========================

def main():

    html = fetch_html()

    result = parse_ip(html)

    for isp, ip in result.items():
    
        if ip and ip != "SKIP":
    
            update_dns(
                DNS_RECORDS[isp],
                ip
            )
    
        else:
    
            print(
                f"⏭️ 跳过 {isp}，没有解析到IP"
            )

    print("全部更新完成！")

    
if __name__ == "__main__":

    try:

        main()

        TG_MESSAGE.insert(
            0,
            "🚀 DNS IP自动更新结果\n"
        )


    except Exception as e:

        TG_MESSAGE.append(
            f"❌运行失败\n{e}"
        )


    finally:

        send_tg()
