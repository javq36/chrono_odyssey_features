from flask import Blueprint, jsonify, request
from services.reddit_scraper_service import fetch_all_posts, filter_posts_by_topics
from db.reddit_db_writer import save_posts_to_db

reddit_scraper_bp = Blueprint('reddit_scraper', __name__)

@reddit_scraper_bp.route('/api/scrape_reddit', methods=['POST'])
def scrape_reddit():
    data = request.get_json()
    
    # Get limits from request, with defaults
    post_limit = data.get('post_limit', 10) if data else 10  # << CAMBIO AQUÍ: Default a 10
    comment_limit = data.get('comment_limit_per_post', 3) if data else 3

    try:
        posts_with_data = fetch_all_posts(
            'chronoodyssey', 
            limit=post_limit, 
            comment_limit_per_post=comment_limit
        )
        
        filtered_posts = filter_posts_by_topics(posts_with_data)

        if filtered_posts:
            # save_posts_to_db ahora devuelve el número de posts guardados/actualizados
            saved_or_updated_count = save_posts_to_db(filtered_posts) 
            print(f"Route: {saved_or_updated_count} posts processed (saved/updated) by database writer.")
        else:
            print("Route: No posts were available after filtering to save or return.")
        
        return jsonify(filtered_posts) # Devuelve todos los posts filtrados

    except Exception as e:
        print(f"Error in scrape_reddit route: {e}")
        # import traceback
        # print(traceback.format_exc())
        return jsonify({"error": "Failed to process Reddit posts", "details": str(e)}), 500
