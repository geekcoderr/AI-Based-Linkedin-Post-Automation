import requests

def post_linkedin_content(access_token, content):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    payload = {
         "author": "urn:li:person:99447075",  # Updated author URN
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": content
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("Content successfully posted on LinkedIn.")
    else:
        print("Failed to post content on LinkedIn. Status code:", response.status_code)
        print("Error message:", response.text)

# Example usage:
access_token = "AQXL0bNJXWkkyVTWdJb1TgPmCWz9oX81mKK4uW_L-1VlGccKdzRc2X2DWNup7PqYAHUNISHvMaWDO_qc6oax8pTz3rQdZG0TGnkdmyjSYN_rNV4-hYgrLVRwLKWhS37vA7EsYhy7TgXcJTTsaQ6v87Sv8BIw5woDSDJcGvhz3lF9aDr9ZSp6XDn5MUC5oaGRagMy37nye8AVsmvXmzko3Q5MRohDv4QeadlcxXG9j_2FCjZYn91rV85tLZMXi_BcoqnkCjK3chI7XXuZBEJFdcib9v4gXgHgn29DG0cgfv4t6G9BlXORUHxfIGe01EPE1zLPtO2ZtP8D8-4QYTPP5pA6RP0AUw"
content = "This is a test post from the LinkedIn API using Python."
post_linkedin_content(access_token, content)
