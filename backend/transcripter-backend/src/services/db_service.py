import sqlite3
import os
from dotenv import load_dotenv
import json
from . import database_schema  # Import the new schema module

# Load environment variables from .env file
load_dotenv()

# Get DB_PATH from environment variable.
DB_PATH = os.getenv('DB_PATH')
if DB_PATH is None:
    raise ValueError("DB_PATH environment variable is not set. Please define it in your .env file.")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir, exist_ok=True)
            print(f"Created directory for database: {db_dir}")
        except OSError as e:
            print(f"Error creating directory {db_dir}: {e}")
            raise
    conn = get_db_connection()
    try:
        database_schema.initialize_all_tables(conn) # This will create all tables from database_schema.py
    finally:
        conn.close()

def save_post(post_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO reddit_posts (id, title, selftext, url)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO NOTHING
        ''', (post_data['id'], post_data['title'], post_data['selftext'], post_data['url']))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.IntegrityError as e:
        print(f"Integrity error saving post ID {post_data.get('id', 'N/A')}: {e}")
        return False
    finally:
        conn.close()

def save_transcript(video_url, transcript_text, video_title=None, channel_name=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    transcript_id = None
    try:
        # Upsert: Insert or update if video_url conflicts
        cursor.execute('''
            INSERT INTO transcripts (video_url, transcript_text, video_title, channel_name)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(video_url) DO UPDATE SET
                transcript_text=excluded.transcript_text,
                video_title=excluded.video_title,
                channel_name=excluded.channel_name,
                created_at=CASE 
                                WHEN excluded.transcript_text != transcripts.transcript_text THEN CURRENT_TIMESTAMP 
                                ELSE transcripts.created_at 
                           END -- Optionally update timestamp if content changes
        ''', (video_url, transcript_text, video_title, channel_name))
        
        # Fetch the id of the inserted or updated row
        cursor.execute("SELECT id FROM transcripts WHERE video_url = ?", (video_url,))
        result = cursor.fetchone()
        if result:
            transcript_id = result['id']
        conn.commit()
    except Exception as e:
        print(f"Error saving transcript for {video_url}: {e}")
    finally:
        conn.close()
    return transcript_id

def get_unprocessed_posts(limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, title, selftext FROM reddit_posts
        WHERE processed_at IS NULL 
        ORDER BY scraped_at ASC
        LIMIT ?
    ''', (limit,))
    posts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return posts

def mark_post_as_processed(post_id, key_points_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        key_points_str = json.dumps(key_points_data) if not isinstance(key_points_data, str) else key_points_data
        cursor.execute('''
            UPDATE reddit_posts
            SET processed_at = CURRENT_TIMESTAMP, key_points = ?
            WHERE id = ?
        ''', (key_points_str, post_id))
        conn.commit()
    except Exception as e:
        print(f"Error marking post {post_id} as processed: {e}")
    finally:
        conn.close()

# --- New functions for new tables ---

def save_external_article(article_data):
    """Saves or updates an external article. article_data is a dict."""
    conn = get_db_connection()
    cursor = conn.cursor()
    article_id = None
    try:
        cursor.execute('''
            INSERT INTO external_articles (url, source, title, content)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                source=excluded.source,
                title=excluded.title,
                content=excluded.content,
                scraped_at=CURRENT_TIMESTAMP
        ''', (article_data['url'], article_data['source'], article_data.get('title'), article_data['content']))
        
        cursor.execute("SELECT id FROM external_articles WHERE url = ?", (article_data['url'],))
        result = cursor.fetchone()
        if result:
            article_id = result['id']
        conn.commit()
    except Exception as e:
        print(f"Error saving external article {article_data.get('url')}: {e}")
    finally:
        conn.close()
    return article_id

def save_topic(topic_name):
    """Saves a topic if it doesn't exist and returns its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    topic_id = None
    try:
        cursor.execute('''
            INSERT INTO topics (name) VALUES (?)
            ON CONFLICT(name) DO NOTHING
        ''', (topic_name,))
        
        cursor.execute('SELECT id FROM topics WHERE name = ?', (topic_name,))
        result = cursor.fetchone()
        if result:
            topic_id = result['id']
        conn.commit()
    except Exception as e:
        print(f"Error saving topic {topic_name}: {e}")
    finally:
        conn.close()
    return topic_id

def associate_topic_to_source(topic_id, source_type, source_id):
    """Associates a topic with a source item (e.g., reddit_post, transcript).
       Returns the association ID if successful, None otherwise.
       Checks for existing association to prevent duplicates."""
    conn = get_db_connection()
    cursor = conn.cursor()
    association_id = None
    try:
        cursor.execute('''
            SELECT id FROM topic_associations 
            WHERE topic_id = ? AND source_type = ? AND source_id = ?
        ''', (topic_id, source_type, source_id))
        existing = cursor.fetchone()
        
        if existing:
            association_id = existing['id']
            print(f"Association already exists for topic {topic_id}, {source_type}, {source_id} with ID {association_id}")
        else:
            cursor.execute('''
                INSERT INTO topic_associations (topic_id, source_type, source_id)
                VALUES (?, ?, ?)
            ''', (topic_id, source_type, source_id))
            association_id = cursor.lastrowid
            conn.commit()
            print(f"Created new association for topic {topic_id}, {source_type}, {source_id} with ID {association_id}")
            
    except Exception as e:
        print(f"Error associating topic {topic_id} to {source_type} {source_id}: {e}")
    finally:
        conn.close()
    return association_id

def save_build(build_data):
    """Saves a new build. build_data is a dict {name, description, build_type}."""
    conn = get_db_connection()
    cursor = conn.cursor()
    build_id = None
    try:
        cursor.execute('''
            INSERT INTO builds (name, description, build_type)
            VALUES (?, ?, ?)
        ''', (build_data['name'], build_data.get('description'), build_data['build_type']))
        build_id = cursor.lastrowid
        conn.commit()
    except Exception as e:
        print(f"Error saving build {build_data.get('name')}: {e}")
    finally:
        conn.close()
    return build_id

def save_build_equipment(equipment_data):
    """Saves equipment for a build. equipment_data is a dict {build_id, slot, item_name}."""
    conn = get_db_connection()
    cursor = conn.cursor()
    equipment_id = None
    try:
        cursor.execute('''
            INSERT INTO build_equipment (build_id, slot, item_name)
            VALUES (?, ?, ?)
        ''', (equipment_data['build_id'], equipment_data['slot'], equipment_data['item_name']))
        equipment_id = cursor.lastrowid
        conn.commit()
    except Exception as e:
        print(f"Error saving build equipment for build {equipment_data.get('build_id')}: {e}")
    finally:
        conn.close()
    return equipment_id

def save_build_skill(skill_data):
    """Saves a skill for a build. skill_data is a dict {build_id, skill_name, rotation_order}."""
    conn = get_db_connection()
    cursor = conn.cursor()
    skill_id = None
    try:
        cursor.execute('''
            INSERT INTO build_skills (build_id, skill_name, rotation_order)
            VALUES (?, ?, ?)
        ''', (skill_data['build_id'], skill_data['skill_name'], skill_data.get('rotation_order')))
        skill_id = cursor.lastrowid
        conn.commit()
    except Exception as e:
        print(f"Error saving build skill for build {skill_data.get('build_id')}: {e}")
    finally:
        conn.close()
    return skill_id

def save_build_trait(trait_data):
    """Saves a trait for a build. trait_data is a dict {build_id, trait_name, points_allocated}."""
    conn = get_db_connection()
    cursor = conn.cursor()
    trait_id = None
    try:
        cursor.execute('''
            INSERT INTO build_traits (build_id, trait_name, points_allocated)
            VALUES (?, ?, ?)
        ''', (trait_data['build_id'], trait_data['trait_name'], trait_data['points_allocated']))
        trait_id = cursor.lastrowid
        conn.commit()
    except Exception as e:
        print(f"Error saving build trait for build {trait_data.get('build_id')}: {e}")
    finally:
        conn.close()
    return trait_id

# Reminder: The actual call to init_db() should be in your app.py
# (e.g., inside create_app()) to ensure it runs once at startup.