import requests
import os


DNSHE_KEY=os.getenv(
    "DNSHE_KEY"
)


#你的CF优选IP网页

URL="https://api.uouin.com/cloudflare.html"


def get_ips():

    r=requests.get(URL)

    text=r.text


    import re


    ips=re.findall(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        text
    )


    return {

        "ct":ips[0],
        "cu":ips[1],
        "cm":ips[2]

    }



def update_dns(
    record,
    ip
):


    url="DNSHE API地址"


    data={

        "record":record,

        "type":"A",

        "value":ip

    }


    r=requests.post(

        url,

        headers={
            "Authorization":
            DNSHE_KEY
        },

        json=data

    )


    print(
        record,
        ip,
        r.text
    )





ips=get_ips()


for record,ip in ips.items():

    update_dns(
        record,
        ip
    )
