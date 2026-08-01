import requests


API_KEY = "cfsd_62683e55f9652467bb7567da9dfdfc19"
API_SECRET = "5bee24c6300089f4ed00673eb823c4ccba072a52d56a95952ec5c904f36a9b5b"

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
