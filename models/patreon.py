import time, requests

PATREON_CLIENT_ID = "tWe8WLdrzldJNM1W2wwQO47x6w3V-jXKWHxqoKpAEQYkstEXQHJndxUN01qvSw2n"
PATREON_CLIENT_SECRET = "nddXb3R832dFtzEo62RBwRX6BIXK86NpeE5dXGrbbTAsUPCEvZYy5A3E8yz8BKSa"
access_token = "Fk0sBdneEdUr29LKWHRJcfjNxAI8_0tbMHkgIX44sa4"
PATREON_REDIRECT_URI = "http://127.0.0.1:5000/connect_patreon"
GDM_CAMPAIGN_ID = 10690153

# api_client = patreon.API(access_token)

# Get the campaign ID
# campaign_response = api_client.fetch_campaign()
# campaign_id = campaign_response.data()[0].id()

reward_cache = {}


def do_rest(url, token=None):
    headers = {
        "Authorization": "Bearer " + token or access_token
    }

    response = requests.get(url, headers=headers)

    json_response = response.json()
    return json_response

def get_tier_data():
    result = do_rest(f"https://api.patreon.com/oauth2/v2/campaigns/{GDM_CAMPAIGN_ID}?include=tiers&fields[tier]=title")
    return result

def get_latest_supporters(access_token):
    return do_rest(f"https://api.patreon.com/oauth2/v2/campaigns/{GDM_CAMPAIGN_ID}/members?include=currently_entitled_tiers&fields[tier]=title&fields[member]=email", access_token)

