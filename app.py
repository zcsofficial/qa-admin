from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import requests

app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection string (hardcoded)
MONGO_URI = "mongodb+srv://adnankstheredteamlabs:Adnan%4066202@cluster0.qrppz7h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['blog_database']
posts_collection = db['posts']

# Imgur client ID (hardcoded)
IMGUR_CLIENT_ID = 'e6dbbffef7d2b47'

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Retrieve all blog posts."""
    posts = list(posts_collection.find())
    for post in posts:
        post['_id'] = str(post['_id'])  # Convert ObjectId to string
    return jsonify({'posts': posts})

@app.route('/api/post', methods=['POST'])
def create_post():
    """Create a new blog post."""
    data = request.form
    # Validate input data
    if 'title' not in data or 'content' not in data:
        return jsonify({'message': 'Title and content are required.'}), 400

    image_url = None
    if 'image' in request.files:
        image_file = request.files['image']
        # Upload image to Imgur and get the URL
        imgur_response = upload_image_to_imgur(image_file)
        if imgur_response and 'link' in imgur_response:
            image_url = imgur_response['link']
            # Optional: Strip the extension from the image URL if present
            if image_url.endswith('.png'):
                image_url = image_url[:-4]  # Remove the last 4 characters (".png")
            elif image_url.endswith('.jpg'):
                image_url = image_url[:-4]  # Remove the last 4 characters (".jpg")

    # Prepare post data
    post = {
        'title': data['title'],
        'content': data['content'],
        'author': data.get('author', 'Anonymous'),
        'image_url': image_url  # Save the image URL
    }

    try:
        posts_collection.insert_one(post)
        return jsonify({'message': 'Post created successfully!'}), 201
    except Exception as e:
        return jsonify({'message': 'Error creating post: ' + str(e)}), 500

def upload_image_to_imgur(image_file):
    """Upload an image to Imgur and return the response."""
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    response = requests.post("https://api.imgur.com/3/image", headers=headers, files={"image": image_file.read()})

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.json()}  # Return error details from Imgur

@app.route('/api/post/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a blog post by ID."""
    try:
        result = posts_collection.delete_one({'_id': ObjectId(post_id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Post deleted successfully!'}), 200
        else:
            return jsonify({'message': 'Post not found!'}), 404
    except Exception as e:
        return jsonify({'message': 'Error deleting post: ' + str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
