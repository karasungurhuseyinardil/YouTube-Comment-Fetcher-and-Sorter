import sys
import os
from googleapiclient.discovery import build
from datetime import datetime
from googleapiclient.errors import HttpError  

API_KEY = "API_KEY"  
VIDEO_ID = 'VIDEO_ID'   


if not API_KEY or API_KEY == "API_KEY":
    print("⚠️ API Key is missing or incorrect. Please set a valid API Key.")
    sys.exit()

if not VIDEO_ID or VIDEO_ID == "VIDEO_ID":
    print("⚠️ Video ID is missing or incorrect. Please set a valid Video ID.")
    sys.exit()

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_comments_and_replies(video_id):
    comments = []
    next_page_token = None
    while True:
        try:
            res = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                maxResults=100,
                order='time',
                pageToken=next_page_token,
                textFormat='plainText'
            ).execute()

            for item in res['items']:
                snippet = item['snippet']['topLevelComment']['snippet']
                comment = {
                    'author': snippet['authorDisplayName'],
                    'text': snippet['textDisplay'],
                    'publishedAt': snippet['publishedAt'],
                    'likeCount': snippet['likeCount'],
                    'replies': []
                }
                if 'replies' in item:
                    for reply in item['replies']['comments']:
                        reply_snippet = reply['snippet']
                        comment['replies'].append({
                            'author': reply_snippet['authorDisplayName'],
                            'text': reply_snippet['textDisplay'],
                            'publishedAt': reply_snippet['publishedAt'],
                            'likeCount': reply_snippet['likeCount']
                        })
                comments.append(comment)

            next_page_token = res.get('nextPageToken')
            if not next_page_token:
                break

        except HttpError as e:
            if e.resp.status == 404:
                print(f"⚠️ Video with ID {video_id} not found. Please check the video ID.")
            elif e.resp.status == 400 and 'badRequest' in str(e):
                print("⚠️ API Key is not valid. Please check your API key.")
            else:
                print(f"⚠️ An error occurred: {e}")
            sys.exit()

    if not comments:
        print("⚠️ No comments found for this video.")
    
    return comments

def sort_comments(comments, sort_by):
    def parse_date(date_str):
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    
    if sort_by == 'time_asc':
        return sorted(comments, key=lambda x: parse_date(x['publishedAt']))
    elif sort_by == 'time_desc':
        return sorted(comments, key=lambda x: parse_date(x['publishedAt']), reverse=True)
    elif sort_by == 'likes_asc':
        return sorted(comments, key=lambda x: (x['likeCount'], parse_date(x['publishedAt'])))
    elif sort_by == 'likes_desc':
        return sorted(comments, key=lambda x: (-x['likeCount'], parse_date(x['publishedAt'])))
    else:
        print("⚠️ Invalid sort type. Defaulting to 'time_desc'.")
        return sorted(comments, key=lambda x: parse_date(x['publishedAt']), reverse=True)

def save_comments_to_file(video_id, comments, sort_by):
    os.makedirs("comments", exist_ok=True)
    filename = f"comments/comments_{video_id}_{sort_by}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for c in comments:
            f.write(f"👤 Author: {c['author']}\n")
            f.write(f"📅 Date: {c['publishedAt']}\n")
            f.write(f"👍 Likes: {c['likeCount']}\n")
            f.write(f"💬 Comment: {c['text']}\n")
            f.write("-" * 40 + "\n")
            if c['replies']:
                f.write("🔽 Replies:\n")
                for reply in c['replies']:
                    f.write(f"   👤 Author: {reply['author']}\n")
                    f.write(f"   📅 Date: {reply['publishedAt']}\n")
                    f.write(f"   👍 Likes: {reply['likeCount']}\n")
                    f.write(f"   💬 Comment: {reply['text']}\n")
                    f.write("-" * 40 + "\n")
    print(f"\n✅ {filename} has been written with {len(comments)} comments.\n")

def main():
    while True:
        print("\nSort Options:")
        print("1 - time_asc   (Ascending by Date)")
        print("2 - time_desc  (Descending by Date)")
        print("3 - likes_asc  (Ascending by Likes)")
        print("4 - likes_desc (Descending by Likes)")
        print("Q - Exit")

        choice = input("Enter your choice: ").strip().lower()
        sort_options = {
            '1': 'time_asc',
            '2': 'time_desc',
            '3': 'likes_asc',
            '4': 'likes_desc',
        }

        if choice == 'q':
            print("Exiting...")
            sys.exit()
        elif choice in sort_options:
            sort_by = sort_options[choice]
            print(f"\n🔄 Fetching and sorting comments: {sort_by}...\n")
            comments = get_comments_and_replies(VIDEO_ID)
            
            if comments:  
                sorted_comments = sort_comments(comments, sort_by)
                save_comments_to_file(VIDEO_ID, sorted_comments, sort_by)
        else:
            print("⚠️ Invalid selection. Please enter 1, 2, 3, 4, or Q.")

if __name__ == "__main__":
    main()
