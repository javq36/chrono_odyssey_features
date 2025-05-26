import praw
import os
from dotenv import load_dotenv
from praw.models import MoreComments # To identify and handle/skip MoreComments objects

load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

# Define un buffer para obtener posts adicionales
POST_FETCH_BUFFER = 5 

def fetch_all_posts(subreddit_name, limit=1000, comment_limit_per_post=5):
    """
    Fetches posts from the specified subreddit using PRAW, 
    including a limited number of top-level comments for each post.
    It fetches 'limit + POST_FETCH_BUFFER' posts from PRAW to increase variety.
    
    Args:
        subreddit_name (str): The name of the subreddit.
        limit (int): The target number of posts, PRAW will be queried for more.
        comment_limit_per_post (int): The maximum number of top-level comments to fetch.
    """
    # Determinar cuántos posts pedir a PRAW
    praw_fetch_limit = limit + POST_FETCH_BUFFER 
    
    print(f"Attempting to fetch up to {praw_fetch_limit} posts from r/{subreddit_name} (target limit: {limit}), with up to {comment_limit_per_post} top-level comments each...")
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
            check_for_async=False
        )
        subreddit = reddit.subreddit(subreddit_name)
        fetched_posts_data = []
        
        # Usar el praw_fetch_limit para la llamada a PRAW
        for post in subreddit.new(limit=praw_fetch_limit): 
            post_data = {
                'id': post.id,
                'title': post.title,
                'selftext': post.selftext,
                'url': post.url,
                'created_utc': post.created_utc, # Added post creation time
                'comments': [] # Initialize comments list for this post
            }

            if comment_limit_per_post > 0:
                fetched_comment_count = 0
                try:
                    # Replace MoreComments objects to load actual top-level comments.
                    # limit=0 means replace all MoreComments at this level (top-level).
                    # This can make additional API calls.
                    post.comments.replace_more(limit=0) 
                    
                    for top_level_comment in post.comments.list(): # .list() provides a flattened list of loaded comments
                        if isinstance(top_level_comment, praw.models.Comment): # Ensure it's an actual comment
                            if fetched_comment_count < comment_limit_per_post:
                                comment_data = {
                                    'id': top_level_comment.id,
                                    'body': top_level_comment.body,
                                    'author': top_level_comment.author.name if top_level_comment.author else None,
                                    'score': top_level_comment.score,
                                    'created_utc': top_level_comment.created_utc
                                }
                                post_data['comments'].append(comment_data)
                                fetched_comment_count += 1
                            else:
                                break # Reached the desired number of comments for this post
                        # If not a praw.models.Comment, it might be a MoreComments object that wasn't replaced,
                        # or something else. We are primarily interested in actual comments here.
                except Exception as comment_e:
                    print(f"Could not fetch comments for post {post.id} (ID: {post.id}): {comment_e}")
            
            fetched_posts_data.append(post_data)
            
        print(f"Successfully fetched {len(fetched_posts_data)} posts from r/{subreddit_name} (PRAW query was for up to {praw_fetch_limit}).")
        return fetched_posts_data
    except Exception as e:
        print(f"Error fetching posts from Reddit: {e}")
        # import traceback
        # print(traceback.format_exc()) # Uncomment for detailed error
        return []

def filter_posts_by_topics(posts_with_data):
    """
    Filters posts based on a predefined list of topics found in title, selftext,
    or the body of their comments. It also stores the matched topic(s)
    in the 'key_points' field of the post.
    """
    if not posts_with_data:
        return []
    
    topics = [
        'gameplay', 'combat', 'economy', 'skills', 'quests', 'modes', 'features', 
        'update', 'patch', 'class', 'character', 'build', 'pvp', 'pve', 
        'dungeon', 'raid', 'crafting', 'gathering', 'lore', 'story', 'bug', 
        'issue', 'suggestion', 'feedback', 'guide', 'tip', 'question', 'help',
        'boss', 'monster', 'item', 'gear', 'weapon', 'armor', 'map', 'zone',
        'event', 'community', 'server', 'latency', 'lag', 'performance'
    ]
    
    filtered_results = []

    for post_item in posts_with_data:
        matched_topics_for_post = set() # Usar un set para evitar tópicos duplicados

        # Asegurar que title y selftext son strings
        title_text = post_item.get('title', '') or ''
        selftext_text = post_item.get('selftext', '') or ''
        
        # Buscar en el título y el texto del post
        text_to_search_in_post = (title_text + ' ' + selftext_text).lower()
        for topic in topics:
            if topic in text_to_search_in_post:
                matched_topics_for_post.add(topic)
        
        # Buscar en los comentarios
        comments_data = post_item.get('comments', [])
        if comments_data:
            for comment in comments_data:
                comment_body = (comment.get('body', '') or '').lower()
                for topic in topics:
                    if topic in comment_body:
                        matched_topics_for_post.add(topic)
        
        # Si se encontró al menos un tópico coincidente
        if matched_topics_for_post:
            # Guardar los tópicos como un string separado por comas
            post_item['key_points'] = ','.join(sorted(list(matched_topics_for_post)))
            filtered_results.append(post_item)
        # else: # Si no hay tópicos coincidentes, no se añade a filtered_results
              # y 'key_points' no se establece o se podría establecer a None explícitamente si fuera necesario
              # post_item['key_points'] = None 
            
    print(f"Filtered down to {len(filtered_results)} posts based on topics in posts or comments.")
    return filtered_results