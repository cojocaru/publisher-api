import os
import json
from config import settings
from datetime import datetime, date, timedelta
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import OpenAIRequest
from dotenv import load_dotenv
import openai
from ordered_item_list_output_parser import OrderedItemListOutputParser
from post_utilities import save_posts, get_grouped_posts, is_valid_url, fetch_and_parse_url, clean_url_to_filename
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate


# Initialize FastAPI app
app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()

# Set OpenAI API Key
openai.api_key = settings.OPENAI_API_KEY



# Endpoint to generate posts using OpenAI API
@app.post("/generate-posts/")
def generate_posts(request: OpenAIRequest):
    topic = request.topic
    network = request.network
    days = request.days

    # Default templates
    system_template = """You are a social media manager. 
                        You generate an ordered list of social media posts. 
                        A user will provide the topic and your job will be to generate posts about 20 characters each, 
                        separated by order number. ONLY return an ordered list, and nothing more."""
    human_template = f"The topic is '{topic}'. Please generate a list of {days} {network} posts that would resonate with an audience interested in {topic}."

    if is_valid_url(topic):
        content = fetch_and_parse_url(topic)
        # Save content to a file in the "documents" folder
        filename = clean_url_to_filename(topic) + '.txt'
        if not os.path.exists('documents'):
            os.makedirs('documents')
        with open(f'documents/{filename}', 'w') as f:
            f.write(content)
        
        # Modify the templates based on the URL content
        human_template = f"Given the following content, please generate a list of {days} {network} posts that would resonate with an audience interested in these topics. Content: {content}"
    

    # Continue with existing logic for generating posts
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", human_template),
    ])

    # Generate posts and save them
    chain = chat_prompt | ChatOpenAI(model='gpt-3.5-turbo-16k') | OrderedItemListOutputParser()
    response_body = chain.invoke({"topic": topic, "network": network, "days": days})
    # TODO: Add database persistence
    save_posts(topic, network, days, response_body)

    # Return all posts grouped by date
    return JSONResponse(content=get_grouped_posts(), status_code=200)

    
# Endpoint to get all posts
@app.get("/get-all-posts/")
def get_all_posts():
    file_path = "posts.json"
    
    # Check if the JSON file exists
    if not os.path.exists(file_path):
        return JSONResponse(content=[], status_code=200)

    # Read and return the existing data
    with open(file_path, "r") as f:
        existing_data = json.load(f)
        
    return JSONResponse(content=existing_data, status_code=200)

# Endpoint to get today's posts
@app.get("/get-todays-posts/")
def get_todays_posts():
    file_path = "posts.json"
    
    # Check if file exists
    if not os.path.exists(file_path):
        return JSONResponse(content={"message": "No posts found"}, status_code=404)

    # Read the JSON data
    with open(file_path, "r") as f:
        existing_data = json.load(f)

    # Filter posts for today
    todays_posts = []
    current_date_str = date.today().strftime("%Y-%m-%d")
    for entry in existing_data:
        for post in entry['posts']:
            if post['publish_date'] == current_date_str:
                # Include topic and network metadata
                post_with_metadata = post.copy()
                post_with_metadata['topic'] = entry['topic']
                post_with_metadata['network'] = entry['network']
                todays_posts.append(post_with_metadata)

    # If no posts for today, return appropriate message
    if not todays_posts:
        return JSONResponse(content={"message": "No posts scheduled for today"}, status_code=200)
    
    return JSONResponse(content=todays_posts, status_code=200)

@app.get("/get-posts-grouped-by-day/")
def get_posts_grouped_by_day():
    return JSONResponse(content=get_grouped_posts(), status_code=200)
