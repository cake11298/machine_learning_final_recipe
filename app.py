from flask import Flask, render_template, jsonify
import test
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
    articles = test.crawler()
    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)
