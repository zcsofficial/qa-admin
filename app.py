from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import logging

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

# MongoDB Atlas connection string
mongo_client = MongoClient("mongodb+srv://adnankstheredteamlabs:Adnan%4066202@cluster0.qrppz7h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client['blog_database']  # Use your database name
posts_collection = db['posts']  # Use your collection name

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = list(posts_collection.find())
    for post in posts:
        post['_id'] = str(post['_id'])  # Convert ObjectId to string
    return jsonify({'posts': posts})

@app.route('/api/post', methods=['POST'])
def create_post():
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'message': 'Title and content are required!'}), 400
        
        post = {
            'title': data['title'],
            'content': data['content'],
            'author': data.get('author', 'Anonymous'),  # Default author
        }
        
        posts_collection.insert_one(post)
        logging.info(f"Post created: {post}")
        return jsonify({'message': 'Post created successfully!'}), 201
    except Exception as e:
        logging.error(f"Error creating post: {e}")
        return jsonify({'message': 'Failed to create post!'}), 500

@app.route('/api/post/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    result = posts_collection.delete_one({'_id': ObjectId(post_id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Post deleted successfully!'}), 200
    else:
        return jsonify({'message': 'Post not found!'}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Get the port from environment variable
    app.run(host='0.0.0.0', port=port)  # Bind to all interfaces and use specified port
