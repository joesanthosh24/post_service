# post_service.py

from flask import Flask, jsonify, request
import requests
import uuid

app = Flask(__name__)

posts = {
    '1': {'user_id': '1', 'post': 'Hello, world!'},
    '2': {'user_id': '2', 'post': 'My first blog post'}
}

posts_api_url = 'https://userservicecontainerapp.purplemoss-ca6cdeba.canadacentral.azurecontainerapps.io'

@app.route('/post/<id>')
def post(id):
    post_info = posts.get(id, {})
    user = {}

    # Get user info from User Service
    if post_info:
        response = requests.get(
            f'{posts_api_url}/user/{post_info["user_id"]}')
        if response.status_code == 200:
            user = response.json()

    return jsonify({'post': post_info, 'user': user})

@app.route('/post', methods=['POST'])
def create_post():
    data = request.json
    user_id = data.get('user_id')

    user_response = requests.get(f'{posts_api_url}/user/{user_id}')

    if user_response.status_code == 200:
        post = data.get('post')
        new_post_id = str(uuid.uuid1())
        posts[new_post_id] = { 'user_id': user_id, 'post': post }

        return jsonify({
            "new_post": posts[new_post_id],
            "all_posts": posts
        })
    
    return jsonify("User doesn't exist")

@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    post_ids = list(posts.keys())

    if id in post_ids:
        data = request.json

        if data.get('post'):
            updated_user_post = data.get('post')
            posts[id]['post'] = updated_user_post

            return jsonify({
                "updated_post": posts[id],
                "all_posts": posts
            })
        
    return jsonify("Post ID doesn't exist")

@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    post_ids = list(posts.keys())

    if id in post_ids:
        post_to_delete = posts[id]
        posts.pop(id)

        return jsonify({
            "deleted_post": post_to_delete,
            "all_posts": posts
        })

    return jsonify("Post ID doesn't exist")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
