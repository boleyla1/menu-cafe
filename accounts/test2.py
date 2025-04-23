import json

import requests

URL = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpWithParams"

url = URL
payload = json.dumps({
    "receptors": [
        {
            "mobile": '09965759902',
            "clientReferenceId": "1"
        }
    ],
    "templateName": "profile",
    "param1": 'hi',
    "isVoice": False,
    "udh": False,

})
headers = {
    'Content-Type': 'application/json',
    'ApiKey': "f70caf7374448b254b53e8d960285173b85915e3b4129b2969266e77398ccdb6FTTqDzfg8uBmCGUy"
}
response = requests.request("POST", url, headers=headers, data=payload)
print("Response Status:", response.status_code)
print("Response Data:", response.text)




