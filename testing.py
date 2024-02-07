import requests
import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ContentTooLong(requests.RequestException):
    """ LinkedIn post limit reached """
    pass

class LinkedIn:
    POST_CHAR_LIMIT = 30000
    BASE_URL = "https://www.linkedin.com"
    COMPANY_PAGE_ID = "99447075"  # Replace this with your company page ID
    POST_ENDPOINT = BASE_URL + f"/voyager/api/feed/company/{COMPANY_PAGE_ID}/shares"

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

    def post_to_company_page(self, text):
        payload = {
            "lifecycleState": "PUBLISHED",
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            },
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "owner": f"urn:li:organization:{self.COMPANY_PAGE_ID}"
        }

        try:
            if len(text) > self.POST_CHAR_LIMIT:
                raise ContentTooLong()

            response = requests.post(self.POST_ENDPOINT, headers=self.headers, json=payload)
            response.raise_for_status()
            print("Succesfully Posted on LinkedIn Company Page.")
        except ContentTooLong:
            print("Error posting to LinkedIn Company Page: post character limit reached")
        except requests.exceptions.RequestException as e:
            print(f"Error posting to LinkedIn Company Page: {e}")

if __name__ == "__main__":
    # Create an instance of the LinkedIn class
    linkedin = LinkedIn()

    # Check if the required argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py 'Text to post on LinkedIn Company Page'")
        sys.exit(1)

    # Get text from command-line arguments
    text = sys.argv[1]

    # Post text on LinkedIn Company Page
    linkedin.post_to_company_page(text)
