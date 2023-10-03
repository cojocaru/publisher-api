import os
import json
import re
import requests
from collections import defaultdict
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Function to save generated posts into a JSON file
def save_posts(topic, network, days, posts):
    file_path = "posts.json"
    data = []
    
    # Check if the JSON file already exists
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    
    # Add new posts to the existing data
    new_entry = {
        "topic": topic,
        "network": network,
        "days": days,
        "posts": posts
    }
    data.append(new_entry)
    
    # Save the updated data back to the JSON file
    with open(file_path, "w") as f:
        json.dump(data, f)


def get_grouped_posts():
    file_path = "posts.json"
    grouped_posts = defaultdict(list)
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            existing_data = json.load(f)
        
        for entry in existing_data:
            for post in entry['posts']:
                post_with_metadata = post.copy()
                post_with_metadata['topic'] = entry['topic']
                post_with_metadata['network'] = entry['network']
                
                publish_date = post['publish_date']
                grouped_posts[publish_date].append(post_with_metadata)

    return dict(grouped_posts)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def fetch_and_parse_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract text from paragraphs (modify as needed)
    paragraphs = soup.find_all('p')
    content = ' '.join([p.get_text() for p in paragraphs])
    return content

def clean_url_to_filename(url):
    return re.sub(r'[^a-zA-Z0-9-_]', '', url)