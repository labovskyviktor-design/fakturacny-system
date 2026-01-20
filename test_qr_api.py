import requests
import sys

def test_api():
    api_url = "https://api.freebysquare.sk/pay/v1/generate-png"
    params = {
        'amount': '15.00',
        'iban': 'SK2111000000002943281214',
        'currencyCode': 'EUR',
        'dueDate': '20260215', # YYYYMMDD
        'variableSymbol': '20260001',
        'size': '300',
        'color': '1',
        'transparent': 'false'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Testing URL: {api_url}")
    print(f"Params: {params}")
    
    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=15)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        
        if response.status_code == 200:
            content_sample = response.content[:10]
            print(f"Content Start (Bytes): {content_sample}")
            if content_sample.startswith(b'\x89PNG'):
                print("SUCCESS: Valid PNG received.")
            else:
                print("FAILURE: Response is 200 OK but NOT a PNG.")
                print(f"Body Text: {response.text[:500]}")
        else:
            print("FAILURE: Non-200 Status Code.")
            print(f"Response Body: {response.text}")
            
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    test_api()
