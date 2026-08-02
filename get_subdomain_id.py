import requests


url = "https://api005.dnshe.com/index.php?m=domain_hub&endpoint=subdomains&action=list"


r = requests.get(
    url,
    headers={
        "X-API-Key": "cfsd_62683e55f9652467bb7567da9dfdfc19",
        "X-API-Secret": "5bee24c6300089f4ed00673eb823c4ccba072a52d56a95952ec5c904f36a9b5b"
    }
)


print("状态码:", r.status_code)
print(r.text)
