import argparse
import json
import os

import requests


URL = "https://affiliate.shopee.vn/api/v3/gql?q=batchCustomLink"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/151.0.0.0 Safari/537.36"
)

COOKIE_HEADER = (
    "language=vi; _gcl_au=1.1.717410842.1779629671; "
    "SPC_F=1lvwarPPnmRUATX37bLZN7S04jNKGU6d; "
    "REC_T_ID=4c0218ad-5775-11f1-86bb-9a9d85dbfc2d; "
    "_ga=GA1.1.1355450000.1780118365; "
    "SPC_CLIENTID=MWx2d2FyUFBubVJVdxqhvymedvofmtmy; "
    "_hjSessionUser_868286=eyJpZCI6IjI5M2ExMzM1LTk1YzYtNTQ5Ni1hMjk1LTA2YmM0MWU2MjNhMyIsImNyZWF0ZWQiOjE3ODAxMTg0MTYzNTEsImV4aXN0aW5nIjp0cnVlfQ==; "
    "_QPWSDCXHZQA=7ca5daa8-865e-45b6-e92d-9a51ea498948; "
    "REC7iLP4Q=05794a98-388c-4798-8751-2c69ed47dfab; "
    "_ga_FV78QC1144=GS2.1.s1786161415$o1$g0$t1786161415$j60$l0$h0; "
    "csrftoken=wFN1qR32jwQUDQQlWy0bIXxmOR1kYaQN; "
    "SPC_SI=tXYnagAAAABtNjFrZlEwQuwZwAcAAAAAMW9OWFZrNUc=; "
    "_med=affiliates; language=vi; _med=refer; "
    "_sapid=19e63dbafa6027d01cbbf1b8749fdde3b3127df78ec12cc2acb66686; "
    "SPC_SC_SA_TK=; SPC_SC_SA_UD=; SPC_SC_OFFLINE_TOKEN=; "
    "SPC_SC_MAIN_SHOP_SA_UD=; SC_SSO=-; SC_SSO_U=-; SPC_SC_SESSION=; "
    "_ga_3XVGTY3603=GS2.1.s1786854354$o3$g1$t1786854529$j50$l0$h0; "
    "SPC_CDS_CHAT=a6ace13a-713c-47f9-8e30-df2f4fc8e7a6; "
    "_hjSession_868286=eyJpZCI6ImQzNGVjODg1LTkxNjAtNDhmYS04MjkyLTUwNWI0NjdlNzljNyIsImMiOjE3ODY4NTkwMTgxNzIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; "
    "sense_sa_r=s; "
    "SPC_ST=lABUba64yDOU3agFUgOSqqiz9+qrk3E9lo30UzOK3m/CcLTvO1OmHhrldRYUq60DMCuBkS1z8dq8h1kDlMW48qGfHZX+98hfbAfY7TdG8N2btVx5cEqn/0xfVxGwGXOF9OgufGombuyb9yKQzImJWDgs2e0p07syVZnMjOgbtCi/Zja2QGQ0yoxki3iwDpX7VmTp4n8zu4rXvgc+VZW/6g==.AC5+pH7ItmraolaMCbNhJAuk6NAyBLQOGhfBQS6s8MKB; "
    "SPC_U=4500495946; "
    "SPC_R_T_ID=Jnf8Uv3tjQ5Qw70lxveb4rTcdM2IA2hefaK24r7tfg07+dIsY+KjLNgucirfrVVPh9gKRirbEGjaK+fAHAF3M8pO0VnNaWc2dQ5kheB3/w6I4+MW8V39621qUtyoX2XpRuEBbBwlJFLMibWBb00Rw7eiiCSO0ep5sTXs3izLhN0=; "
    "SPC_R_T_IV=V3l2c1Z3amlWR25PN3BtSQ==; "
    "SPC_T_ID=Jnf8Uv3tjQ5Qw70lxveb4rTcdM2IA2hefaK24r7tfg07+dIsY+KjLNgucirfrVVPh9gKRirbEGjaK+fAHAF3M8pO0VnNaWc2dQ5kheB3/w6I4+MW8V39621qUtyoX2XpRuEBbBwlJFLMibWBb00Rw7eiiCSO0ep5sTXs3izLhN0=; "
    "SPC_T_IV=V3l2c1Z3amlWR25PN3BtSQ==; "
    "shopee_webUnique_ccd=%2BeeRXZdG0OYrt9c0UdSSTw%3D%3D%7CKXK1JqhvbmLx37MMkm4fYCRpL3LsKgUjRMLTwPCqnFdhUNeqEkCUSX4vrRGw0ODMZ%2BA14EY7vtFO1Og%3D%7Cp%2BhwESzTR27KrtCS%7C08%7C3; "
    "ds=ac9fdfb4d29d18ecb09382762a97e7fe; "
    "_ga_4GPP1ZXG63=GS2.1.s1786859023$o21$g1$t1786859668$j28$l0$h1225504181"
)

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    "af-ac-enc-dat": "8246436c1fe77ded",
    "af-ac-enc-sz-token": (
        "78tS7J7lW9Jgb4AvZeioDQ==|KHK1JqhvbmLx37MMkm4fYCRpL3LsKgUjRMLTwMBXnFdhUNeqEkCUSX4vrRGw0ODMZ+A14EY7vtFO1Og=|"
        "p+hwESzTR27KrtCS|08|3"
    ),
    "affiliate-program-type": "1",
    "content-type": "application/json; charset=UTF-8",
    "cookie": COOKIE_HEADER,
    "csrf-token": "T7ko8360-pmpVASeeqaHwIjdi29mXZEoCAZw",
    "origin": "https://affiliate.shopee.vn",
    "priority": "u=1, i",
    "referer": "https://affiliate.shopee.vn/offer/custom_link",
    "sec-ch-ua": '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": USER_AGENT,
    "x-sap-ri": "9450816adcb313b310c64c3805017d43da83e5ec5363b9abe91e",
    "x-sap-sec": "6TrpaTb5iJa/akpQbJwQbkXQNJYdbOuQ9mw1bJRQxJYKbP6Q0mwObEpQlJwVbrpQiJY8beNQmJGNbEXQ6JwfbOwQXmGYbJuQ1JYabe5QWmGybIzQfJGBbE2QdJwybk2Q9JGIbruQRcG3bI5QGJYlbe2QUmGKbH2QzJYpbkrQUFY9bO2QjFY9bJwQJJjQbJwQbJZuEZthbJwQGweSgXsCbFwQbJwQEQn1iIi/bFwQUJzQbI8UvlbQbkYHvJjQbJwQrUVQbPYQbJwk+MudbJwQNkGtTJwQbpwdbJwxbmwQaU2hRFwQbS4KbcwQvJzQbJwQ7G7v0AZ1bJwQzbpnMc2xbcwQbJwUEducbJGXrcCFK6zVd7P+b5KWbFwQbJwGgzuRbJC/bcwQbOZl04dUkOmd69i3bJYT+pRQbJw7FjHo7kKGjYTa0PT78wKCl8b6DPbZq7Sf9VFi6dH4c2aSiM6JQwnYFPY42p69h8v03CpvpsOKcJ2A5fhsqnbg848qiUxqfoOskm2Uplx3S7ok3z/v/F/17KoSEHtGiHsjMFMxDc2SH5bFovzRu1v3Rmb/cOcUd1OrlR52MkSbTVqFpe0i0rofeGugRJKVhoqXgBkze8cOOwborFg5b2g+nsSL7Iy9d44eataH8L/LEOXyE3uTHHPPvD/MPtpPXqsfSHr09dewp3R0AMGitZJyIaXBtZHpC/fkIrdGqFisbPDPzZythbjr89EXbJ2QbJYdt9a3gboOImuQbJYJ2ieBQJwQbrN0ISXb58N//kH7kpwGBLwL/YM507IUdft7V68IkRJb2voUU2ucTsNP/xePpcPcSks3UEumXYO9I0d71E3McN1d+WvVUDCY28BbjpDVURui5WSTEzf5q449Okf6TtuUTfb5ZnsmSpXopjz+DyL+3EBm5wao0iBAb12Yae0q9lXR/GGB0ThVVZTtECJUsmqQ0+euojyfhXbRIj1hVHnOhJlyupeGdj8KvR48h4VBbJwQ4HogkFpQbJw2Libn9qF3ODGE9zbQbJwQbJwQbJwQbJYPbJwQWwuMnFxg/ZqIsATqFpvYRgB2lTNkIeFE9ukyqd8fob1redbTXq8rIQ8SgAiWk/Dq8xzQgjtcE14HedXmbotkIMKeCRAHk3Ftv01Xv+nZ7Z6LI9zzDcwQbJwQbJwQbJwQwmwQbOIKykRxQh8UtZuF8Ac8HV2Is5pQyJwQbJK09RRmk/fWwGRz9kCx2YH7EX5bXYFI5JJH9RNirEftZG0FXcwQbJwvbJwQxxzjykFmS6oEeiuy9qfROcI3zkwykhv8Z/kV95GmHqksL+zlXbxcPFW2zRy9dtnunG6lykfAKYRQbJwQZJwQboiZAIQfSHDLbJwQbJwQbJwibJwQzdJv7p7P0R2C00azN40UfRNhqBqLkFDoH/+CvP3l4g1Mm/VvETAQbJ2QbJwqc8j41hUjEc2QbJYzj4bUT4w8TJwQbJC=",
    "x-sz-sdk-version": "1.12.21",
}

PAYLOAD = {
    "operationName": "batchGetCustomLink",
    "query": """
    query batchGetCustomLink($linkParams: [CustomLinkParam!], $sourceCaller: SourceCaller){
      batchCustomLink(linkParams: $linkParams, sourceCaller: $sourceCaller){
        shortLink
        longLink
        failCode
      }
    }
    """,
    "variables": {
        "linkParams": [
            {
                "originalLink": "https://shopee.vn/Qu%E1%BA%A7n-Short-N%E1%BB%AF-Qu%E1%BA%A7n-Short-Jeans-L%C6%B0ng-Cao-T%C3%BAi-Sau-Th%C3%AAu-T%E1%BB%AB-40-65kg-Th%E1%BA%A3o-Xinh-Store-Ms-442-i.1019246541.24748107264",
                "advancedLinkParams": {},
            }
        ],
        "sourceCaller": "CUSTOM_LINK_CALLER",
    },
}


def build_payload(original_link: str) -> dict:
    payload = json.loads(json.dumps(PAYLOAD))
    payload["variables"]["linkParams"][0]["originalLink"] = original_link
    return payload


def build_request_body(original_link: str) -> str:
    return json.dumps(build_payload(original_link), ensure_ascii=False, separators=(",", ":"))


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Shopee Affiliate custom link.")
    parser.add_argument(
        "original_link",
        nargs="?",
        default=os.getenv("ORIGINAL_LINK"),
        help="Shopee original link. Can also be passed with ORIGINAL_LINK env.",
    )
    args = parser.parse_args()

    if not args.original_link:
        parser.error("missing original_link. Example: py -3.14 main.py https://s.shopee.vn/...")

    session = create_session()
    response = session.post(URL, data=build_request_body(args.original_link), timeout=30)

    print("Status:", response.status_code)
    try:
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except requests.JSONDecodeError:
        print(response.text)


if __name__ == "__main__":
    main()
