import requests 
import json
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()    
apikey = os.getenv('apikey')
channel_handle = 'MrBeast'
max_results = 50

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
def get_video_ids(play_list_id):
    page_token = None
    video_ids = []
    base_url = 'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=' + str(max_results) + '&playlistId=' + play_list_id + '&key=' + apikey
    try:
        while True:
            url = base_url
            if page_token:
                url += '&pageToken=' + page_token
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            data = response.json()
            json_object = json.dumps(data, indent=4)
            for item in data['items']:
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            page_token = data.get('nextPageToken')
            if not page_token:
                break
        return video_ids
        

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
def getting_video_data(video_ids):
    def batch_list(video_ids, batch_size):
        for i in range(0, len(video_ids), batch_size):
            yield video_ids[i:i + batch_size]
    
    extracted_data = []
    
    if video_ids:
        for batch in batch_list(video_ids, max_results):
            url = 'https://youtube.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id=' + ','.join(batch) + '&key=' + apikey
            try:
                response = requests.get(url)
                response.raise_for_status()  # Check if the request was successful
                data = response.json()
                for item in data['items']:
                    video_id = item['id']
                    snippet = item['snippet']
                    content_details = item['contentDetails']
                    statistics = item['statistics']
                    video_data = {
                        'video_id': video_id,
                        'title': snippet['title'],
                        'published_at': snippet['publishedAt'],
                        'duration': content_details['duration'],
                        'view_count': statistics.get('viewCount', 0),
                        'like_count': statistics.get('likeCount', 0),
                        'comment_count': statistics.get('commentCount', 0)
                    }
                    extracted_data.append(video_data)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
        
        return extracted_data
    else:
        print("No video IDs found.")
        return []
def save_to_json(extracted_data):
    import os
    # Create data directory if it doesn't exist
    data_dir = r'C:\Users\LOQ\Documents\youtube_DE\data'
    os.makedirs(data_dir, exist_ok=True)
    
    # Use a valid Windows filename format (replace colons with hyphens)
    timestamp = datetime.today().isoformat().replace(':', '-')
    filepath = os.path.join(data_dir, f'video_data_{timestamp}.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, indent=4, ensure_ascii=False)
    print(f"Data saved to: {filepath}")
    


if __name__ == "__main__":
    video_data = None
    play_list_id = get_playlist_id()
    if play_list_id:
        video_ids = get_video_ids(play_list_id)
        if video_ids:
            print(f"Found {len(video_ids)} videos")
            video_data = getting_video_data(video_ids)
            if video_data:
                print(f"\nVideo Details:")
                print(json.dumps(video_data, indent=2))
                print(f"\nTotal videos fetched: {len(video_data)}")
                save_to_json(video_data)
            else:
                print("Failed to retrieve video data")
        else:
            print("Failed to retrieve video IDs")
    else:
        print("Failed to retrieve playlist ID") 
    