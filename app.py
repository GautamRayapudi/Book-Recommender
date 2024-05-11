from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Load data from pickle files
current_dir = os.path.abspath(os.getcwd())
files = ['popular.pkl', 'pt.pkl', 'books.pkl', 'similarity_scores.pkl']
names = ['popular_df', 'pt', 'books', 'similarity_scores']

for i, j in zip(files, names):
    pickle_file_path = os.path.join(current_dir, i)
    globals()[j] = pd.read_pickle(pickle_file_path)
        
isbn_df = pd.merge(books,popular_df,on=['Book-Title','Image-URL-M','Book-Author',],how='inner')

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(isbn_df['Book-Title'].values),
                           author=list(isbn_df['Book-Author'].values),
                           image=list(isbn_df['Image-URL-M'].values),
                           votes=list(isbn_df['num_ratings'].values),
                           rating=list(isbn_df['avg_rating'].values),
                           isbn=list(isbn_df['ISBN'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')




@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    if user_input is not None and user_input.strip():  # Check if user input is provided and not empty
        try:
            index = np.where(pt.index == user_input)[0][0]
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

            data = []
            for i in similar_items:
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                item = [
                    temp_df['Book-Title'].values[0],
                    temp_df['Book-Author'].values[0],
                    temp_df['Image-URL-M'].values[0],
                    temp_df['ISBN'].values[0]
                ]
                data.append(item)

            if data:
                return render_template('recommend.html', data=data)
            else:
                return render_template('recommend.html', message="No recommendations found.")

        except IndexError:
            return render_template('recommend.html', message="Book not found.")
    else:
        return render_template('recommend.html', message="Please enter a book title.")

if __name__ == '__main__':
    app.run(debug=True)
