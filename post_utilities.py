import os
import json
from collections import defaultdict

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

