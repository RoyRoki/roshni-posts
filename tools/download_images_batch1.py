import os
import urllib.request
import json
import ssl

# JSON data from browser subagent
posts_data = [
  {"post": 1, "url": "https://lh3.googleusercontent.com/gg/AMW1TPo3P5gGQ9HaEJsone_PgSl3K6PFSbyoH7rfHNeJs_sg0FaEYPnFubQaNBLTMznOj-NEcN0BlO6XdW3YbrGpSza0AkH_J8ual4ESUflmrCXNFNDt7Uu51JQllZKCmT5xZmF_SnHW5QZG87-AMci825gDIuSVbvs6j3FohRwX9ZL3Oev8yY4=s1024-rj-mp2"},
  {"post": 2, "url": "https://lh3.googleusercontent.com/gg/AMW1TPq66QbsErrlrioCyx2ArEEpbJbjn6GxR0aWytolfZBq0K0wv9TcGPhd65_KVWip4n-x7vLD0N1lkYyKMK2RuWSDVNtBwZWYsZ_sMScu3biqiZnbPZbRByRYVlApiJaquLKzceV0Uif3rtyOO0jswf27t02jmQOu-pD1gQZTg_7XRPXI4TqM=s1024-rj-mp2"},
  {"post": 3, "url": "https://lh3.googleusercontent.com/gg/AMW1TPqjCPALVhTmN76PM0-vhsRZdeDJdS-nlGBDwh3pfNeSUutpAn6CWol6AwBwVW6KMXk5SWU6r5oSuyNl9xUtpe_4f7xRO7NF8kOjySXUMOFKROdaIV4o-4LvQFa5KBrknBFsRRoT5xJdM5H2i_62kDSjrWR9ccgwV8xmX0ET_vkuqgYpCeiA=s1024-rj-mp2"},
  {"post": 4, "url": "https://lh3.googleusercontent.com/gg/AMW1TPR6jCQVgBEqt6tXROXkZp3SplL2a67d25iUUkUr9P6xqr2WGOeDxh9CIVNVrkieUTuokFCTdPR4ux5sYJ-120kz4V7nrUR9bXpNiJS8LVWu-4Hs_OFlOOfB45PUs5QzpC1ml6w5H9xWxyBxPESKnLqjiSFV_vWQRFx9sBnS9LDvDreKYKG=s1024-rj-mp2"},
  {"post": 5, "url": "https://lh3.googleusercontent.com/gg/AMW1TPqfDdKGX13a3WCogvv3Xgbc6RuBJUisXPLJcQMVKO7X1Wv2DpnpmaP3pykjGjK8K-VMbokH3xX_MHpym7dZxkdULJtFSKo83S39m5YptpUxovg6YknhbJBA1iQ0ZNNOgBEIuZJIrfWnzNvcr3k_doIlFt1fZ4k2CG8-Y2rfHZQ-4dHeZL9_=s1024-rj-mp2"},
  {"post": 6, "url": "https://lh3.googleusercontent.com/gg/AMW1TPrB68S2yn5YKY-AHDZVYqnHu8xzg2oxSePsu9zGZU5FDRX4vDwf0AkKTJ4iGx5gPkt74wsD9Shi0UzgKBgPHFV3jMEd__fLCBqNc4ocZdAZnsdlYoM5mJQWypozurvoDrKdz2-Nd6UPzaGTz-BXFVBrM6RpnbjtE77nZn_M66uTW5aIk8EM=s1024-rj-mp2"},
  {"post": 7, "url": "https://lh3.googleusercontent.com/gg/AMW1TPpLOA7XUVxjhzL4PuTqay5Sqqm39FOa0CI_Y7TTBa9U7DjbbjjDoFrYXxF6x9xZxJewWzQvgVQA8kV6EQDHzoY30c_RCOksEq_vvKYbhCjAxM6pf48DU8QjlmXSMwiF4ysvWzXzHoIM8xmSVNBImMo2GJVWjhjZNPyYtq4t_kFYgDRPGhM=s1024-rj-mp2"},
  {"post": 8, "url": "https://lh3.googleusercontent.com/gg/AMW1TPpnl1dJsiKj6LWAqVCfPFIx_ZJzGvX9kt9EKMNk29iP0CZjZf2ApqeKDIA4UddVz6URd4cVipxPlpegmSct8dUTWgZd9ncD3v501I4xDDQlXCYnFoYRSZeRnJl1fyoddDun44ztyCgVzC4vchMuQo4mp7Xk5ZMaWsItF9MU6fpoahSSZmoE=s1024-rj-mp2"},
  {"post": 9, "url": "https://lh3.googleusercontent.com/gg/AMW1TPqaDPiD5bSIydbHGKkGBk4aqa6SCOHYqdPooiFnzrq7lKwDIATwhYSudxVJZVZUrYCCCctIHw2a2H_zBxijDNNtcdHsl51SR_2o3FY4ALKEu3jQHpKnZAs_kREoocTQO8WNbYPzQ-oWR6-4gvj9gbyyF8iT_ezvifSMiXGe6Gq11lx_lF8=s1024-rj-mp2"},
  {"post": 10, "url": "https://lh3.googleusercontent.com/gg/AMW1TPqgxovEp7TbYNfcHeK9_NvR2fcqzSXFsT2SQt4oSvNhCVxbXo84Z4WvBeTQmVuko9iEsvSGy29iCbOJYJtogtKvq8KvOzlpT9bCGkqJ2ffyjOcQGWSbhc11FtfunrA9cZmVRbI-TG74nxQ3dmMuBYQr5nJeIQrf7lCw9s2fK8UdzCElGCu6=s1024-rj-mp2"}
]

POSTS_DIR = "posts"

def download_images():
    # Bypass simple SSL verify issues if any
    ssl._create_default_https_context = ssl._create_unverified_context
    
    for item in posts_data:
        post_num = item['post']
        url = item['url']
        
        target_dir = os.path.join(POSTS_DIR, f"post{post_num}")
        if not os.path.exists(target_dir):
            print(f"Directory {target_dir} does not exist, creating...")
            os.makedirs(target_dir, exist_ok=True)
            
        target_file = os.path.join(target_dir, "image.png")
        
        try:
            print(f"Downloading Post {post_num} image...")
            # Use urllib
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(target_file, 'wb') as out_file:
                out_file.write(response.read())
                
            print(f"Saved to {target_file}")
            
        except Exception as e:
            print(f"Failed to download Post {post_num}: {e}")

if __name__ == "__main__":
    download_images()
