import re
from datetime import datetime, timedelta
from langchain.schema import BaseOutputParser

class OrderedItemListOutputParser(BaseOutputParser):
    def parse(self, text: str):
        pattern = r'\d+\. \"(.*?)\"'
        raw_posts = re.findall(pattern, text)
        
        posts = []
        current_date = datetime.now()
        
        for i, post_body in enumerate(raw_posts):
            post_date = current_date + timedelta(days=i)
            posts.append({
                "body": post_body,
                "publish_date": post_date.strftime("%Y-%m-%d")
            })
            
        return posts
