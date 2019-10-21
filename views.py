from flask import Blueprint, request, json, Response, jsonify, render_template
from app import db
from models import Post

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/like_post', methods=['POST'])
def like_post():
    post_id = request.json['post_id']
    likes = request.json['total_likes']
    if post_id and likes:
        post_liked = Post.query.filter_by(id=post_id).first()
        post_liked.likes = likes
        db.session.commit()
        return Response('Ok', 200)
    return 'Missing data'

@main.route('/new_post', methods=['POST'])
def create_new_post():
    # Quando faz um post para o server guarda para a database
    # actualiza a visualizacion em cliente-side com jquery
    # get data from the request and save it to the database
    author = request.json['author']
    title = request.json['title']
    text = request.json['text']
    # Like is seted by the database default
    if author and title and text:
        if type(author) == str and type(title) == str and type(text) == str:
            if len(author) <= 20 and len(title) <= 50 and len(text) <= 300 :
                #save the data in the database
                print('Saving to database')
                new_post = Post(author=author, title=title, text=text)
                db.session.add(new_post)
                db.session.commit()
                ind = str(new_post.id)
                q_new_post = Post.query.filter_by(id=new_post.id).first()
                return jsonify({'status':'Ok','post_id':ind, 'likes':q_new_post.likes})         
    return 'Missing data'

@main.route('/get_posts', methods=['GET'])
def get_all_post():
    post_list = Post.query.all()
    posts = []
    for post in post_list:
        posts.append({'post_id':str(post.id), 'author': post.author, 'title': post.title, 
                      'text':post.text, 'likes':str(post.likes)})
    return jsonify(posts)
