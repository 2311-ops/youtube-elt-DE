import requests 
import json
import os 
from dotenv import load_dotenv
load_dotenv()
apikey = os.getenv('apikey')
channel_handle = 'MrBeast'
def get_playlist_id():
    try:
        url='https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle=' + channel_handle + '&key=' + apikey
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        json_object = json.dumps(data, indent=4)
        channel_item= data["items"][0]
        uploads_playlist_id = channel_item["contentDetails"]["relatedPlaylists"]["uploads"]
        return uploads_playlist_id
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None 
if __name__ == "__main__":
    print("Playlist ID:", get_playlist_id())
else:
    print("This module is being imported, not run directly.")