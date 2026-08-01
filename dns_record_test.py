import requests


API_KEY = "你的KEY"
API_SECRET = "你的SECRET"

subdomain_id = 7007606429


url = (
    "https://api005.dnshe.com/index.php"
    "?m=domain_hub"
    "&endpoint=dns_records"
    "&action=list"
)


r = requests.get(
    url,
    headers={
        "X-API-Key": API_KEY,
        "X-API-Secret": API_SECRET
    },
    params={
        "subdomain_id": subdomain_id
    }
)


print("状态码:", r.status_code)
print(r.text)
