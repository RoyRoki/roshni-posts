import os
import requests
from dotenv import load_dotenv

# Load env from current directory
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
API_VERSION = "v18.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

def get_instagram_account_id():
    if not ACCESS_TOKEN:
        print("Error: ACCESS_TOKEN not found in .env")
        return None

    # 1. Get User's Pages
    url = f"{BASE_URL}/me/accounts"
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "name,id,instagram_business_account"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "error" in data:
            print(f"API Error: {data['error']['message']}")
            return None
            
        print(f"Found {len(data.get('data', []))} Pages linked to this user.")
        
        for page in data.get('data', []):
            page_name = page.get('name')
            page_id = page.get('id')
            ig_account = page.get('instagram_business_account')
            
            print(f"Page: {page_name} (ID: {page_id})")
            
            if ig_account:
                ig_id = ig_account.get('id')
                print(f"  -> Linked Instagram Business Account ID: {ig_id}")
                return ig_id
            else:
                print("  -> No Instagram Business Account linked.")
                
        print("No linked Instagram Business Account found on any page.")
        return None
        
    except Exception as e:
        print(f"Request Failed: {e}")
        return None

if __name__ == "__main__":
    ig_id = get_instagram_account_id()
    if ig_id:
        print(f"\nSUCCESS: Use Instagram Account ID: {ig_id}")
    else:
        print("\nFAILURE: Could not retrieve Instagram Account ID.")
