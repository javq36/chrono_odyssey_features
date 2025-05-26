from flask import Blueprint, jsonify, request
from services.reddit_scraper_service import fetch_all_posts, filter_posts_by_topics

reddit_scraper_bp = Blueprint('reddit_scraper', __name__)

@reddit_scraper_bp.route('/api/scrape_reddit', methods=['POST'])
def scrape_reddit():
    data = request.get_json()
    limit = data.get('limit', 5)
    posts = fetch_all_posts('chronoodyssey', limit=limit)
    filtered_posts = filter_posts_by_topics(posts)
    return jsonify(filtered_posts)
