import openai
import os
from flask import request, jsonify, Blueprint
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

summarize_bp = Blueprint('summarize', __name__)

@summarize_bp.route('/api/chatgpt_summarize', methods=['POST'])
def chatgpt_summarize():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    prompt = (
        "Analyze the following game transcript and provide:\n"
        "1. A concise summary of the main ideas.\n"
        "2. A bullet-point list of the main features (skills, combat, economy, modes, etc.) mentioned.\n\n"
        f"Transcript:\n{text}\n\nSummary and Features:"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "..."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=900,
            temperature=0.5,
        )
        result = response.choices[0].message.content.strip()
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@summarize_bp.route('/api/chatgpt_keypoints', methods=['POST'])
def chatgpt_keypoints():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    prompt = (
        "Analyze the following game transcript and extract the key points, grouped by the following interests:\n"
        "- Gameplay\n"
        "- Combat\n"
        "- Economy\n"
        "- Skills\n"
        "- Quests\n"
        "- Modes\n"
        "- Other Features\n\n"
        "For each group, provide a bullet-point list of the most important details mentioned in the transcript. "
        "Do NOT provide a general summary. Only list key points under each group.\n\n"
        f"Transcript:\n{text}\n\nKey Points by Interest:"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Use "gpt-4o" or "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are an expert game analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=900,
            temperature=0.3,
        )
        result = response.choices[0].message.content.strip()
        return jsonify({'keypoints': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500