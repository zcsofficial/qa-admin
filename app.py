from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB connection string
mongo_client = MongoClient("mongodb+srv://adnankstheredteamlabs:Adnan%4066202@cluster0.qrppz7h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client['your_database_name']  # Replace with your actual database name
posts_collection = db['posts']

@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        posts = list(posts_collection.find({}, {'_id': 0}))  # Exclude the MongoDB ID from the response
        return jsonify({"posts": posts}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/post', methods=['POST'])
def create_post():
    try:
        data = request.json
        author = data.get('author', 'Unknown Author')  # Set a default value if 'author' is not provided

        new_post = {
            'title': data['title'],
            'content': data['content'],
            'author': author,
            'created_at': datetime.utcnow()
        }

        posts_collection.insert_one(new_post)
        return jsonify({"message": "Post created successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/post/<string:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        result = posts_collection.delete_one({'_id': post_id})  # Use the ObjectId for deletion

        if result.deleted_count > 0:
            return jsonify({"message": "Post deleted successfully!"}), 200
        else:
            return jsonify({"message": "Post not found!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
