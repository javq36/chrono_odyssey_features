def create_reddit_posts_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reddit_posts (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            selftext TEXT,
            url TEXT UNIQUE,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed_at TIMESTAMP,
            key_points TEXT 
        )
    ''')
    print("Ensured reddit_posts table exists.")

def create_transcripts_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_url TEXT UNIQUE NOT NULL,
            video_title TEXT,
            channel_name TEXT,
            transcript_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed_at TIMESTAMP,
            key_points TEXT
        )
    ''')
    print("Ensured transcripts table exists.")

def create_external_articles_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS external_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL, -- e.g., 'official_site', 'wiki', etc.
            url TEXT UNIQUE NOT NULL,
            title TEXT,
            content TEXT NOT NULL,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            key_points TEXT
        )
    ''')
    print("Ensured external_articles table exists.")

def create_topics_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("Ensured topics table exists.")

def create_topic_associations_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topic_associations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            source_type TEXT NOT NULL CHECK(source_type IN ('reddit_post', 'transcript', 'external_article')),
            source_id TEXT NOT NULL,
            FOREIGN KEY(topic_id) REFERENCES topics(id)
        )
    ''')
    print("Ensured topic_associations table exists.")

def create_builds_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS builds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            build_type TEXT CHECK(build_type IN ('pvp', 'pve', 'hybrid')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("Ensured builds table exists.")

def create_build_equipment_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS build_equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            build_id INTEGER NOT NULL,
            slot TEXT NOT NULL,
            item_name TEXT NOT NULL,
            FOREIGN KEY(build_id) REFERENCES builds(id)
        )
    ''')
    print("Ensured build_equipment table exists.")

def create_build_skills_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS build_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            build_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            rotation_order INTEGER,
            FOREIGN KEY(build_id) REFERENCES builds(id)
        )
    ''')
    print("Ensured build_skills table exists.")

def create_build_traits_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS build_traits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            build_id INTEGER NOT NULL,
            trait_name TEXT NOT NULL,
            points_allocated INTEGER NOT NULL,
            FOREIGN KEY(build_id) REFERENCES builds(id)
        )
    ''')
    print("Ensured build_traits table exists.")

def initialize_all_tables(conn):
    cursor = conn.cursor()
    create_reddit_posts_table(cursor)
    create_transcripts_table(cursor)
    create_external_articles_table(cursor)
    create_topics_table(cursor)
    create_topic_associations_table(cursor)
    create_builds_table(cursor)
    create_build_equipment_table(cursor)
    create_build_skills_table(cursor)
    create_build_traits_table(cursor)
    conn.commit()
    print("All database tables initialized/ensured.")
