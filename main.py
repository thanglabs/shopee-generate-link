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

COOKIES = [
    ("language", "vi", ".shopee.vn"),
    ("_gcl_au", "1.1.717410842.1779629671", ".shopee.vn"),
    ("SPC_F", "1lvwarPPnmRUATX37bLZN7S04jNKGU6d", ".shopee.vn"),
    ("REC_T_ID", "4c0218ad-5775-11f1-86bb-9a9d85dbfc2d", ".shopee.vn"),
    ("_ga", "GA1.1.1355450000.1780118365", ".shopee.vn"),
    ("SPC_CLIENTID", "MWx2d2FyUFBubVJVdxqhvymedvofmtmy", ".shopee.vn"),
    (
        "_hjSessionUser_868286",
        "eyJpZCI6IjI5M2ExMzM1LTk1YzYtNTQ5Ni1hMjk1LTA2YmM0MWU2MjNhMyIsImNyZWF0ZWQiOjE3ODAxMTg0MTYzNTEsImV4aXN0aW5nIjp0cnVlfQ==",
        ".shopee.vn",
    ),
    ("_QPWSDCXHZQA", "7ca5daa8-865e-45b6-e92d-9a51ea498948", "affiliate.shopee.vn"),
    ("REC7iLP4Q", "05794a98-388c-4798-8751-2c69ed47dfab", "affiliate.shopee.vn"),
    ("_ga_FV78QC1144", "GS2.1.s1786161415$o1$g0$t1786161415$j60$l0$h0", ".shopee.vn"),
    ("csrftoken", "wFN1qR32jwQUDQQlWy0bIXxmOR1kYaQN", ".shopee.vn"),
    ("SPC_SI", "tXYnagAAAABtNjFrZlEwQuwZwAcAAAAAMW9OWFZrNUc=", ".shopee.vn"),
    ("_med", "affiliates", ".shopee.vn"),
    ("language", "vi", "affiliate.shopee.vn"),
    ("_med", "refer", ".affiliate.shopee.vn"),
    ("_sapid", "19e63dbafa6027d01cbbf1b8749fdde3b3127df78ec12cc2acb66686", "affiliate.shopee.vn"),
    ("SPC_SC_SA_TK", "", ".shopee.vn"),
    ("SPC_SC_SA_UD", "", ".shopee.vn"),
    ("SPC_SC_OFFLINE_TOKEN", "", ".shopee.vn"),
    ("SPC_SC_MAIN_SHOP_SA_UD", "", ".shopee.vn"),
    ("SC_SSO", "-", ".shopee.vn"),
    ("SC_SSO_U", "-", ".shopee.vn"),
    ("SPC_SC_SESSION", "", ".shopee.vn"),
    ("_ga_3XVGTY3603", "GS2.1.s1786854354$o3$g1$t1786854529$j50$l0$h0", ".shopee.vn"),
    (
        "_hjSession_868286",
        "eyJpZCI6ImE2OGYwNzlhLTFmMTgtNDY5NS05OTgxLWQ3ZmViYmZlZGFhOSIsImMiOjE3ODY4NTQ1MzMwMjMsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=",
        ".shopee.vn",
    ),
    (
        "SPC_ST",
        "rrTZofLnA6F5KpqOpfFvTr9qXRU3FNjsbks2Z6Iqrs6ZxQ23bclFBRvVDwVtSSpXVw8aeoPGe4PcAg4poZ2rrIkyrQ3gm1zNuIQfGBuNkARQiwBYt3oUM4FSKfWncu/8jNWs81cpjoCN/KeqIexPd/ggqEdZRP876K/VC24qAHXEr1NclIWJJDfBJKcjgn1CqICVTb28pml2+DBRQ4MrSw==.AMwETEQBRVZivGIJVmKquWCfQKxh8/OyyKvPgK0pqmL6",
        ".shopee.vn",
    ),
    ("SPC_U", "4500495946", ".shopee.vn"),
    (
        "SPC_R_T_ID",
        "pAuhsWzoPQ7yL/0yirN1gT+KpQumHX+TI67ogq1Xtjzyy9VAOIJ5+2qd5B4j6RzyWs/E3lVJo9GDADEzGv3KxQYEUn4amjmVyPi9mRspKfDck85vaGEJhLaIQraf7cv+XQVKIvwOaa25iIsukt2gNNoUawZcnknWN4dYwEmrecU=",
        ".shopee.vn",
    ),
    ("SPC_R_T_IV", "YnhCSXNjZnpVSmgxQXlpeg==", ".shopee.vn"),
    (
        "SPC_T_ID",
        "pAuhsWzoPQ7yL/0yirN1gT+KpQumHX+TI67ogq1Xtjzyy9VAOIJ5+2qd5B4j6RzyWs/E3lVJo9GDADEzGv3KxQYEUn4amjmVyPi9mRspKfDck85vaGEJhLaIQraf7cv+XQVKIvwOaa25iIsukt2gNNoUawZcnknWN4dYwEmrecU=",
        ".shopee.vn",
    ),
    ("SPC_T_IV", "YnhCSXNjZnpVSmgxQXlpeg==", ".shopee.vn"),
    ("SPC_CDS_CHAT", "a6ace13a-713c-47f9-8e30-df2f4fc8e7a6", ".shopee.vn"),
    ("sense_sa_r", "s", ".shopee.vn"),
    (
        "AC_CERT_D",
        "gqRjZGVrxHeFomtpuDE0MjUxOmNhcHRjaGFfY29va2llX2tleaJrdtEAAqRhbGdv0gAAAGSjZGVrwKJjdMRAAAAADMz6+srpuPrvM57Cf+ZesyCjzpS7fSHExkhhfUPNjcYjTFT2GSfMIrdZ/hvxKL+WYVjT9V3dRSDauGpQzKpjaXBoZXJ0ZXh0xQM+AAAADNt2HQrsYGQFUBoR612hjraJxm/KToenKSeNIZcbsb+EOKe0tlqZjVdEZ/U9CWtZxrTsumx3rdaHWjNfTh6Xh0VE5E4SSiRq0sfhciRbxySvTx1rhCG01RCfvRPly+8rfgjtG6BmrxS3LVu7Zuh3UCq5lTntQW/UILks7PgVlUyofqPLEuPR2dj8lg1U3iOsnr3LQzEm88rz+bkD4C+bjZAo3wzjYnfDBDdD9EJnlMTDcI4V3wWxJCruhblFpG2PY1iY+fS2VgqHFn2gWHdnV28U45U9YZN47HfmgMtQFJ/1agv4w64+oGFztbHUv7ooayjEXWtmIlwcnSgMZy6bVbxphv5MvaAevX4tgEEW3LB24Rm6ZbMS188sq+azitBS+2gyIzCHIV5ZMWPy5gz4RY+nVnNCxjQX+YSIRRSWi0uhUivtXJ1uaW1YqxPiBsEdTLym85bbIjEecLJQx+JpiHenR8V2xtYsBAWGQUtgw0qjfnJ8DFLOlSfJsH/eEw6PgSB/v92HDBlPccK2sNVSPqU5W27UVk7PiICt8fhghu2sCX/nkrDk5TtzXQhBmBBejKYF2PrkjlIMv2M5l1b1QSNth0tZ592+Gy1yF84jNrzS8jL2wn/7wJEOmhO2coxrP0ruB45JqoAYXDt1HiW3rbq/hGogtEUXljddLH9F8sj6U4PIE7T0UfqqM4sySOJ40Y08LftXNmGNK5agmN9UzNyJkNGoiNOLJdPe1shthz8/E1AzM4j1lHk8enN+GRIGTQSCuwOcRoKcKsarqDGFW0x/6rM1owYo3g5RCWXrGrRl1gefpzXyFZ9FOnTYmdrwT2/+VaogTHCP7D2Dt0gXjgN7rcz/ozlzUi5Qbl/2mucxw9cKa3qNPG/EEDq1UTJywR0hmBPcmvMsyP3TNVrIgKv02t7j/ETy7VLcJ0hXXhUGB6vPNMZZUW2jvRMCW1NvgtAezRhs8NFp06BQ6YwrgtDnUb2JF0I0SCDhQ7dvJ/JbD+UvfTRq2Dv4cMkzu6fO7fKRRTPNFqs+iJzVN6x4epEPdPb+qojCkR6YDF/DQHYnHiiMiHEuvFPsIg89C3sL8SjBcWkQdgguHl0=",
        ".shopee.vn",
    ),
    (
        "shopee_webUnique_ccd",
        "YF0XzsUXlRqcevomLDIEDQ%3D%3D%7CJHK1JqhvbmLx37MMkm4fYCRpL3LsKgUjRMLTwMIUXlZhUNeqEkCUSX4vrRGw0ODMZ%2BA14EY7vtFO1ug%3D%7Cp%2BhwESzTR27KrtCS%7C08%7C3",
        "affiliate.shopee.vn",
    ),
    ("ds", "1313903797f568893d173c28fbe02461", "affiliate.shopee.vn"),
    ("_ga_4GPP1ZXG63", "GS2.1.s1786854532$o20$g1$t1786855429$j57$l0$h1644400809", ".shopee.vn"),
]

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    "af-ac-enc-dat": "c7cef5d54e8f45f7",
    "af-ac-enc-sz-token": (
        "cCmJ+xVn7Gtw2bbucDSSFA==|IXK1JqhvbmLx37MMkm4fYCRpL3LsKgUjRMLTwJ/PYVZhUNeqEkCUSX4vrRGw0ODMZ+A14EY7vtFOVA==|"
        "p+hwESzTR27KrtCS|08|3"
    ),
    "affiliate-program-type": "1",
    "csrf-token": "VWM979zE-caLJXMN91TM4p8L_1Gg8jHzhNhg",
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
    "x-sap-ri": "0a40816ae4633c08edbad83b0501f625a1741728b3f892a32428",
    "x-sap-sec": "UoPg2c6bx46KfPuvg42vgPrv340WgkbvQy2CgHuvY42RgOuvx40LgSjvw4LugHrvM42sgr2vUyLkg4pvW404gSAv1yLSg5Rva4LngHwvK42SgPwvv4LxgOpvLdLFg5Avz40EgSwvXyLWgEwvG40jgPXvXT00grwvZT01grpvvy2dg4zvi400g42vp4Nvg42vg438tjqGg42vw2A0hvsOgT2vg42vSlkYfU9DgT2vX4RvgIpGQwbvgkB294Nvg42vPe5vgs0vg42sz+p1g42vM9MXn42vgs21g42Igy2valstuT2vgS1Wgd2va4Rvg42v/BedQbLBg42vm6X9NmjIgd2vg42ASmpUg4LtTdKV0b6Fj7u4g5fKgT2vg42jjRpVg4KDgd2vgOcab4QGYHm3YvgUg401zszvg4L6rjbUXwhd0xy9OeWSERkjC9I3BEVRx6EDzJVVe39vqQu2VcJiRXk0FRxpKmxh25H9VDTuawQrqrbA+Kbwuka3sPCOH7Dx2R5QChkEaJEr+mBg/hWjBPF5ws8Ud2Y2YvpJuM+Is2LcU3ynwScv2pcMESHZbWXRWF3v11k5XCBQgKtr3XpvzBVCTAQjjbmXM1rnvfSlZqbZpe4gwVACPeXupsLlOl4wB2I6OAWD46kodfml7ldUWamSEXrWgX57fQbdBee8o/VO4P3ED9xMOEuzXNCyZgKUU865FZ3DCKVlyAK4L/Z4khQ5a4FHg4wvg40EWsEJMYAzuTpvg4KWIPf8042vgOvSmPKigdCjCsQai7yeS4q0t+qXx9ctLyTQyRcOkyOvpFTXqhyyJe+j5rINyMxD2xnjWVb0fvvPBMQGO4tzILDyPvWvl24i2/UzpjrR82StK7rmC7cFjDKOQhuV5ibik69d/SA5nfIQv0d20s4DsOrqEoDG3ex6qzWBFqxXuMxhwk9MrjXp4TIh7by21NtCKWzWp1HQE25OGfxsYfsJcpv7hyAU/2C2Hf0tA2png42v4ypGa4uvg42MxxxK3c0XbINK0Cbvg42vg42vg42vg40Gg42v9+CgQqrSX++SUtF00lNInMYHEtBZwi7iWkMddL7HmBdhnKxd/c7Zwlp0hng6ZX6QXcDlexdqjPaJnKWJOmdxwgiLOKDfZ97R1jZrB3Rk8+AN8vl52T2vg42vg42vg42vmy2vgO1ESeQruy0NuQCJ3nq7fOXSUhpvC42vgJiS0KQoZXp7GBIR7e5rDczQtUIH/J0YCFV20KBexjpRbBhJ6d2vg42Qg42vacDNoe0ogfi4nxn43cHtbm1hHeChZyR6bmMH7s4ofJYkx/lI/OruaJoHHKm3tdNcqBEQoeHKAcVvg42vj42vgoNeVpNHgf6Ag42vg42vg42wg42vFTlNRTychuuo+ORPJ3S09dHLbqaBZ9Avj42vg4uqRugVgW6Afy2vgJN7tFN/xONv",
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


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)

    for name, value, domain in COOKIES:
        session.cookies.set(name, value, domain=domain, path="/")

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
    response = session.post(URL, json=build_payload(args.original_link), timeout=30)

    print("Status:", response.status_code)
    try:
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except requests.JSONDecodeError:
        print(response.text)


if __name__ == "__main__":
    main()
