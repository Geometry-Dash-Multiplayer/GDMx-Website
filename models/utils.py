import re
from extensions import oauth
from run import EMOJI_MAP


def replace_emojis(text):
    for emoji_name, emoji_code in EMOJI_MAP.items():
        if f":{emoji_name}:" in text:
            print(f"Replacing :{emoji_name}: with {emoji_code}")
        text = re.sub(f":{emoji_name}:", emoji_code, text)
    return text

patreon = oauth.remote_app(
    'patreon',
    consumer_key='tWe8WLdrzldJNM1W2wwQO47x6w3V-jXKWHxqoKpAEQYkstEXQHJndxUN01qvSw2n',
    consumer_secret='nddXb3R832dFtzEo62RBwRX6BIXK86NpeE5dXGrbbTAsUPCEvZYy5A3E8yz8BKSa',
    request_token_params={
        'scope': 'users pledges-to-me my-campaign',  # Adjust scopes as needed
    },
    base_url='https://www.patreon.com/api/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://www.patreon.com/api/oauth2/token',
    authorize_url='https://www.patreon.com/oauth2/authorize',
)