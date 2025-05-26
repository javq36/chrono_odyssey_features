import sqlite3
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')) # Ensure .env from src is loaded

# Get DB_PATH from environment variable.
DB_FILE_PATH = os.getenv('DB_PATH')

if DB_FILE_PATH is None:
    raise ValueError("DB_PATH environment variable is not set in .env file. Please define it (e.g., C:\\sqlite\\Databases\\chronodb.db)")

print(f"reddit_db_writer.py: Attempting to connect to DB at: {DB_FILE_PATH}")

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    db_folder = os.path.dirname(DB_FILE_PATH)
    if db_folder and not os.path.exists(db_folder):
        try:
            os.makedirs(db_folder, exist_ok=True)
            print(f"reddit_db_writer.py: Created directory for database: {db_folder}")
        except OSError as e:
            print(f"reddit_db_writer.py: Error creating directory {db_folder}: {e}")
            raise 

    conn = sqlite3.connect(DB_FILE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def save_comments_to_db(conn, comments_to_save, parent_post_id):
    """
    Saves a list of comments to the reddit_comments table for a given post_id.
    If a comment already exists (based on id), it updates its body, author, and score.
    """
    if not comments_to_save:
        return 0

    cursor = conn.cursor() # Use the passed-in connection's cursor
    saved_or_updated_comment_count = 0
    for comment in comments_to_save:
        try:
            comment_id = comment.get('id')
            if not comment_id:
                print(f"Skipping comment due to missing ID for post {parent_post_id}")
                continue
            
            body = comment.get('body', '')
            author = comment.get('author') # Author might be None
            score = comment.get('score')
            created_utc = comment.get('created_utc') # Original creation time

            cursor.execute("""
                INSERT INTO reddit_comments (id, post_id, body, author, score, created_utc)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    body = excluded.body,
                    author = excluded.author,
                    score = excluded.score
                    -- We do NOT update 'post_id' or 'created_utc' for an existing comment.
                ;
            """, (
                comment_id,
                parent_post_id,
                body,
                author,
                score,
                created_utc
            ))
            if cursor.rowcount > 0:
                saved_or_updated_comment_count += 1
        except sqlite3.Error as e:
            print(f"Database error saving or updating comment {comment.get('id')} for post {parent_post_id}: {e}")
        except Exception as e:
            print(f"Unexpected error processing comment {comment.get('id')} for saving/updating: {e}")
    # The commit is handled by the calling function (save_posts_to_db)
    return saved_or_updated_comment_count

def save_posts_to_db(posts_to_save):
    """
    Saves a list of posts and their comments to the database.
    If a post already exists (based on id), it updates its content, 
    key_points (matched filter topics), and scraped_at.
    """
    if not posts_to_save:
        print("No posts provided to save.")
        return 0

    conn = None
    total_posts_saved_or_updated = 0
    total_comments_saved_or_updated = 0 # Cambiar nombre para reflejar actualizaciones
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for post in posts_to_save:
            try:
                post_id = post.get('id')
                title = post.get('title', 'N/A')
                selftext = post.get('selftext', '')
                url = post.get('url', '')
                created_utc = post.get('created_utc') # Original creation time, does not change
                key_points_value = post.get('key_points', None) # Matched filter topics
                current_scraped_at = datetime.now(timezone.utc).isoformat()

                if not post_id:
                    print(f"Skipping post due to missing ID: {title[:30]}")
                    continue

                cursor.execute("""
                    INSERT INTO reddit_posts (id, title, selftext, url, created_utc, scraped_at, processed, key_points)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        title = excluded.title,
                        selftext = excluded.selftext,
                        url = excluded.url,
                        key_points = excluded.key_points,
                        scraped_at = excluded.scraped_at
                        -- We do NOT update 'created_utc' as it's the original creation time.
                        -- We do NOT update 'processed' here, as its update is part of a different workflow.
                    ;
                """, (
                    post_id,
                    title,
                    selftext,
                    url,
                    created_utc,
                    current_scraped_at,
                    0,  # For new posts, 'processed' is 0. For existing, it's not touched by this UPDATE.
                    key_points_value
                ))
                
                if cursor.rowcount > 0:
                    total_posts_saved_or_updated += 1
                
                comments = post.get('comments', [])
                if comments:
                    # Pass the connection to save_comments_to_db
                    saved_for_this_post = save_comments_to_db(conn, comments, post_id)
                    total_comments_saved_or_updated += saved_for_this_post # Sumar el resultado de comentarios

            except sqlite3.Error as e:
                print(f"Database error saving or updating post {post.get('id')}: {e}")
            except Exception as e:
                print(f"Unexpected error processing post {post.get('id')} for saving/updating: {e}")

        conn.commit() # Commit once after all posts and their comments are processed
        print(f"Successfully saved or updated {total_posts_saved_or_updated} posts and saved or updated {total_comments_saved_or_updated} comments.")
        return total_posts_saved_or_updated
    except sqlite3.Error as e:
        print(f"General database connection or commit error in reddit_db_writer: {e}")
        return 0
    finally:
        if conn:
            conn.close()