from utils import patreon
import time

client_id = "tWe8WLdrzldJNM1W2wwQO47x6w3V-jXKWHxqoKpAEQYkstEXQHJndxUN01qvSw2n"
client_secret = "nddXb3R832dFtzEo62RBwRX6BIXK86NpeE5dXGrbbTAsUPCEvZYy5A3E8yz8BKSa"
access_token = "Fk0sBdneEdUr29LKWHRJcfjNxAI8_0tbMHkgIX44sa4"
PATREON_REDIRECT_URI = "http://127.0.0.1:5000/connect_patreon"

api_client = patreon.API(access_token)

# Get the campaign ID
campaign_response = api_client.fetch_campaign()
campaign_id = campaign_response.data()[0].id()

reward_cache = {}

def get_reward_details(api_client, reward_id):
    """Fetches individual tier details using reward_id."""
    if reward_id in reward_cache:
        return reward_cache[reward_id]
    try:
        reward_response = api_client.fetch_reward(reward_id)
        tier_name = reward_response.data().attribute('title')
        reward_cache[reward_id] = tier_name
        return tier_name
    except Exception as e:
        print(f"Error fetching reward details for ID {reward_id}: {e}")
        return None

def get_latest_supporters():
    all_pledges = []
    cursor = None
    while True:
        pledges_response = api_client.fetch_page_of_pledges(campaign_id, 25, cursor=cursor)
        cursor = api_client.extract_cursor(pledges_response)
        all_pledges += pledges_response.data()
        if not cursor:
            break

    supporters_info = []
    unique_reward_ids = set()

    for pledge in all_pledges:
        reward_data = pledge.relationship('reward').json_data
        reward_id = reward_data.get('data', {}).get('id', None) if reward_data else None
        if reward_id:
            unique_reward_ids.add(reward_id)
        else:
            print(f"No reward ID found for pledge {pledge.id()}")
            tier_name = "No Tier"
            reward_cache[None] = tier_name

    for reward_id in unique_reward_ids:
        get_reward_details(api_client, reward_id)

    for pledge in all_pledges:
        patron = pledge.relationship('patron')
        full_name = f"{patron.attribute('first_name')} {patron.attribute('last_name')}"
        total_pledged_cents = pledge.attribute("amount_cents")
        total_pledged = f"${total_pledged_cents / 100:.2f}"

        reward_data = pledge.relationship('reward').json_data
        reward_id = reward_data.get('data', {}).get('id', None) if reward_data else None
        tier_name = reward_cache.get(reward_id, None)

        supporters_info.append({
            "full_name": full_name,
            "tier": tier_name,
            "total_pledged": total_pledged
        })

    for supporter in supporters_info:
        print(f"Name: {supporter['full_name']}, Tier: {supporter['tier']}, Total Pledged: {supporter['total_pledged']}")

get_latest_supporters()
