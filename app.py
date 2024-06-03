from flask import Flask, render_template, jsonify, request, redirect, flash
import test, recognize
from werkzeug.utils import secure_filename
import os
import pandas as pd
import joblib
import xgboost

app = Flask(__name__)
app.secret_key = os.urandom(20)
articles = [
    {"id": 0, "img": "https://example.com/image1.jpg", "text": "文章1的描述", "ingredients": ["ingredient1", "ingredient2"], "directions": ["step1", "step2"], "nutrition": ["calories: 100"]},
    {"id": 1, "img": "https://example.com/image2.jpg", "text": "文章2的描述", "ingredients": ["ingredient1", "ingredient2"], "directions": ["step1", "step2"], "nutrition": ["calories: 200"]},
    {"id": 2, "img": "https://example.com/image3.jpg", "text": "文章3的描述", "ingredients": ["ingredient1", "ingredient2"], "directions": ["step1", "step2"], "nutrition": ["calories: 300"]}
]

ingredients = []

@app.route('/')
def index():
    return render_template('index.html', articles=articles)

@app.route('/refresh', methods=['POST'])
def refresh():
    global articles
    articles = test.crawler(ingredients)  # 確保 test.crawler() 返回正確的數據格式
    return jsonify(articles)

@app.route('/getRecipe', methods=['GET'])
def get_recipe():
    article_id = request.args.get('articleId')
    if article_id is not None:
        try:
            article_id = int(article_id)
            if 0 <= article_id < len(articles):
                # print(articles[article_id])
                return jsonify(articles[article_id])
            else:
                return jsonify({'error': 'Invalid articleId'}), 404
        except ValueError:
            return jsonify({'error': 'Invalid articleId format'}), 400
    return jsonify({'error': 'No articleId provided'}), 400


app.config['UPLOAD_FOLDER'] = './uploads'

@app.route('/upload', methods=['POST'])
def upload_file():
    global ingredients
    ingredients = []
    if 'imageUploadInput' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['imageUploadInput']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        recognized = recognize.recognize_image(filepath)
        ingredients.append(recognized)

    recipe_type = request.form.get('timingOption', 'No Type Selected')
    cuisine_type = request.form.get('typeOption', 'No Cuisine Selected')
    gender = request.form.get('genderSelectOption', 'No Gender Selected')
    height = float(request.form.get('height', 0)) 
    weight = float(request.form.get('weight', 0))
    fat = float(request.form.get('fat', 0))
    age = int(request.form.get('age', 0)) 
    if(recipe_type != "nooption"):
        ingredients.append(recipe_type)
    if(cuisine_type != "nooption"):
        ingredients.append(cuisine_type)

    model = joblib.load('calorie_model.pkl')
    data = pd.DataFrame({
        'height': [height],
        'weight': [weight],
        'body_fat_percentage': [fat],
        'age': [age]
    })
    prediction = model.predict(data)

    prediction_value = float(prediction[0])
    ingredients = list(set(ingredients))

    print(ingredients)
    
    return jsonify({'recognized': recognized, 'prediction': prediction_value})

if __name__ == '__main__':
    app.run(debug=True)
