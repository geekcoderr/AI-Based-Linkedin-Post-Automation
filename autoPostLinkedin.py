import requests
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()

class ContentTooLong(requests.RequestException):
    """ LinkedIn post limit reached """
    pass

class LinkedIn:
    POST_CHAR_LIMIT = 30000
    BASE_URL = "https://www.linkedin.com"
    POST_ENDPOINT = BASE_URL + "/voyager/api/contentcreation/normShares"

    def __init__(self):
        self.cookies = {
            "JSESSIONID": os.getenv("JSESSIONID"),
            "li_at": os.getenv("li_at")
        }
        self.headers = {
            "accept": "application/vnd.linkedin.normalized+json+2.1",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json; charset=UTF-8",
            "csrf-token": self.cookies["JSESSIONID"],
            "origin": self.BASE_URL,
            "cookie": '; '.join([f'{key}="{value}"' if key == "JSESSIONID" else f'{key}={value}' for key, value in
                                 self.cookies.items()]),
            "Referer": self.BASE_URL + "/feed/",
            "Referrer-Policy": "strict-origin-when-cross-origin, strict-origin-when-cross-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        }

    def post(self, text):
        payload = {
            "visibleToConnectionsOnly": False,
            "externalAudienceProviders": [],
            "commentaryV2": {
                "text": text,
                "attributes": []
            },
            "origin": "FEED",
            "allowedCommentersScope": "ALL",
            "postState": "PUBLISHED"
        }
        try:
            if len(text) > self.POST_CHAR_LIMIT:
                raise ContentTooLong()
            response = requests.post(self.POST_ENDPOINT, headers=self.headers, json=payload)
            response.raise_for_status()
            print("Succesfully Posted on LinkedIn.")
        except ContentTooLong:
            print("Error posting to LinkedIn: post character limit reached")
        except requests.exceptions.RequestException as e:
            print(f"Error posting to LinkedIn: {e}")

if __name__ == "__main__":
    
    linkedin = LinkedIn()

    
    if len(sys.argv) != 2:
        print("Usage: python script.py 'Text to post on LinkedIn'")
        sys.exit(1)

    
    text = sys.argv[1]

    
    linkedin.post(text)
