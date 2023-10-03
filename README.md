# FastAPI Social Media Post Generator

## Overview

This FastAPI application generates social media posts using the OpenAI API. It provides endpoints for generating new posts based on user-defined topics, retrieving all posts, filtering posts for today, and grouping posts by their publish date.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Usage](#usage)
  - [Generate Posts](#generate-posts)
  - [Get All Posts](#get-all-posts)
  - [Get Today's Posts](#get-todays-posts)
  - [Get Posts Grouped by Date](#get-posts-grouped-by-date)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

## Installation

### Prerequisites

- Python 3.x
- FastAPI
- Uvicorn
- OpenAI Python package

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/cojocaru/publisher-api.git
    ```

2. Navigate to the project directory:

    ```bash
    cd publisher-api
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables:

    Create a `.env` file in the root directory and add your OpenAI API key:

    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

5. Run the application:

    ```bash
    uvicorn main:app --reload
    ```

## Usage

### Generate Posts

To generate new posts (limit 20 leters for now), make a POST request to `/generate-posts/` with the following JSON payload (the topic can be aslo URL):

```json
{
  "topic": "science",
  "network": "linkedin",
  "days": 7
}
```

### Get All Posts

To retrieve all generated posts, make a GET request to `/get-all-posts/`.

### Get Today's Posts

To filter posts for today's date, make a GET request to `/get-todays-posts/`.

### Get Posts Grouped by Date

To get posts organized by their publish date, make a GET request to `/get-posts-grouped-by-day/`.

## Future Enhancements

- Add database support for more robust data storage.
- Implement authentication for better security.
- Add rate-limiting to prevent abuse.

## Contributing

Contributions are welcome!
