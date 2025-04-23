import json
import requests


def send_otp(mobile, param1, ):
    url = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpWithParams"

    print(f"Sending OTP to: {mobile}, Code: {param1}")

    payload = json.dumps({
        "receptors": [
            {
                "mobile": str(mobile),
                "clientReferenceId": "1"
            }
        ],
        "templateName": "boleyla",
        "param1": str(param1),
        "isVoice": False,
        "udh": False,
        'linenumber': '30005006004099'
    })
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': "35a3e8b000ce1ed436329a2796b38e634ca4f35bfb9f7adb2cd91ee64cbc26f5kdbHYwiRyWt7bbMz"
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
