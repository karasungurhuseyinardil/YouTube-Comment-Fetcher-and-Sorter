# YouTube Comment Fetcher and Sorter

This Python script fetches YouTube comments for a specific video, sorts them according to various criteria (e.g., by time or likes), and saves them to a text file.

## Prerequisites

Before using the script, make sure to install the required Python libraries:

1. `google-api-python-client`
2. `datetime`
3. `os`
4. `sys`

You can install the necessary libraries using pip:

```bash
pip install google-api-python-client
```

## Setup

### 1. YouTube API Key

You will need a YouTube Data API v3 key for this script to work. You can get one by following these steps:

* Go to the [Google Developers Console](https://console.developers.google.com/).
* Create a new project.
* Enable the **YouTube Data API v3** for the project.
* Create an **API key** and paste it in the script.

Replace the placeholder value for `API_KEY` in the script:

```python
API_KEY = "YOUR_API_KEY"
```

### 2. Video ID

Replace the placeholder `VIDEO_ID` with the actual YouTube video ID of the video you want to fetch comments for. The video ID can be found in the video URL (e.g., `https://www.youtube.com/watch?v=p5kGYewj6r4` where `p5kGYewj6r4` is the video ID).

```python
VIDEO_ID = 'YOUR_VIDEO_ID'
```

## Usage

1. Run the script:

```bash
python youtube_comment_fetcher_and_sorter.py
```

2. The script will ask you how you want to sort the comments:

   * `1`: Sort comments by **ascending date**.
   * `2`: Sort comments by **descending date**.
   * `3`: Sort comments by **ascending number of likes**.
   * `4`: Sort comments by **descending number of likes**.
   * `Q`: Exit the script.

3. Once you select a sort option, the script will fetch the comments, sort them, and save them to a text file in the `comments/` folder.

   The file will be named: `comments/comments_<VIDEO_ID>_<SORT_OPTION>.txt`.

## Output

The output file contains the following information for each comment:

* **Author**: The name of the user who posted the comment.
* **Date**: The publication date of the comment.
* **Likes**: The number of likes the comment has.
* **Comment text**: The actual text of the comment.
* **Replies**: If there are any replies to the comment, they will be listed under the comment.

Example:

```
👤 Author: John Doe
📅 Date: 2022-10-15 14:23:01
👍 Likes: 5
💬 Comment: Great video!
----------------------------------------
🔽 Replies:
   👤 Author: Jane Smith
   📅 Date: 2022-10-15 15:00:00
   👍 Likes: 3
   💬 Comment: I agree!
----------------------------------------
```


## Limitations

* The YouTube API has quota limits, so make sure to monitor your API usage if you're fetching a large number of comments.
* The script fetches the first 100 comments per page. If there are more comments, it will continue fetching them in batches.


