from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb+srv://adnankstheredteamlabs:Adnan%4066202@cluster0.qrppz7h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['your_database_name']  # Change to your actual database name
posts_collection = db['posts']

# Serve the admin panel
@app.route('/')
def admin_panel():
    return render_template('admin.html')

# Serve the blog page
@app.route('/blog')
def blog():
    return render_template('blog.html')

# API to get all posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = list(posts_collection.find())
    for post in posts:
        post['_id'] = str(post['_id'])  # Convert ObjectId to string
    return jsonify({'posts': posts})

# API to create a new post
@app.route('/api/post', methods=['POST'])
def create_post():
    data = request.json
    post = {
        'title': data['title'],
        'content': data['content'],
        'author': data.get('author', 'Admin')  # Default to 'Admin' if not provided
    }
    result = posts_collection.insert_one(post)
    post['_id'] = str(result.inserted_id)
    return jsonify({'message': 'Post created successfully.', 'post': post}), 201

# API to delete a post
@app.route('/api/post/<string:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        result = posts_collection.delete_one({'_id': ObjectId(post_id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Post deleted successfully.'}), 200
        else:
            return jsonify({'message': 'Post not found.'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
