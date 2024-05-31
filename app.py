from flask import Flask, render_template, jsonify
import test
from flask import request
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

articles = [
    {"img": "https://example.com/image1.jpg", "text": "文章1的描述","ingredients":"做法1","nutrition":""},
    {"img": "https://example.com/image2.jpg", "text": "文章2的描述","ingredients":"做法2","nutrition":""},
]

@app.route('/')
def index():
    return render_template('index.html', articles=articles)

@app.route('/refresh', methods=['POST'])
def refresh():
    global articles
    articles = test.crawler()
    return jsonify(articles)

@app.route('/getRecipe', methods=['POST'])
def get_recipe():
    print(articles[0])
    return jsonify(articles[0])

app.config['UPLOAD_FOLDER'] = './uploads'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

if __name__ == '__main__':
    app.run(debug=True)