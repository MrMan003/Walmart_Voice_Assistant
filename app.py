from flask import Flask, render_template, request, flash, session, url_for
import os, time, json

from utils.nlp_processor import extract_entities
from utils.store_mapping import shelf_position, entrance_position, find_product_location, store_grid
from utils.navigation import compute_path, generate_directions
from utils.voice_generator import generate_voice

app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config['UPLOAD_FOLDER'] = 'static/audio'

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_url = None
    route_coords = None

    # Only play welcome voice if it's a GET request (i.e., page load or refresh)
    play_welcome = request.method == 'GET'

    # Initialize chat history once per session
    session.setdefault('chat_history', [])

    if request.method == 'POST':
        play_welcome = False  # Don't play welcome on POST (user interaction)

        voice_text = request.form.get("voice_text", "")
        entities = extract_entities(voice_text)
        source = destination = None

        # Extract source and destination based on roles
        for e in entities:
            text = e['text'].strip()
            label = e['label']
            role = e.get('role')

            if role == 'Source':
                if label == 'Product':
                    source = find_product_location(text.lower())
                elif label == 'Aisle':
                    source = shelf_position.get(text.upper())
                elif label == 'Entrance':
                    source = entrance_position

            elif role == 'Destination':
                if label == 'Product':
                    destination = find_product_location(text.lower())
                elif label == 'Aisle':
                    destination = shelf_position.get(text.upper())
                elif label == 'Entrance':
                    destination = entrance_position

        if source and destination:
            path = compute_path(store_grid, source, destination)
            if path:
                directions = generate_directions(path)
                generate_voice(directions)
                audio_url = url_for('static', filename='audio/final_instructions.mp3') + f"?t={int(time.time())}"
                route_coords = [{"x": col, "y": 0, "z": row} for (row, col) in path]

                session['chat_history'].append({
                    'user': voice_text,
                    'bot': {
                        'products': [e['text'] for e in entities if e['label'] == 'Product'],
                        'aisles': [e['text'] for e in entities if e['label'] == 'Aisle'],
                        'directions': directions
                    }
                })
                session.modified = True
            else:
                flash("Path not found.")
        else:
            flash("Source or destination not identified.")

    return render_template(
        "index.html",
        audio_url=audio_url,
        route_coords=json.dumps(route_coords) if route_coords else None,
        chat_history=session.get('chat_history', []),
        play_welcome=play_welcome  # Passed to template
    )

if __name__ == "__main__":
    app.run(debug=True)
