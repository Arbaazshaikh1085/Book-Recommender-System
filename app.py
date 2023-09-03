from flask import Flask,render_template,request
import numpy as np
import pandas as pd

popular_50=pd.read_csv('popular_50.csv')
pt=pd.read_csv('pt.csv')
books=pd.read_csv('books_name.csv')
simillarity_score=np.loadtxt('simillarity_score.csv',delimiter=',')

pt.set_index('Book-Title',inplace=True)

app=Flask(__name__,template_folder='template')

@app.route('/')
def index():
    return render_template('index.html',
                           book_title=list(popular_50['Book-Title'].values),
                           author=list(popular_50['Book-Author'].values),
                           image=list(popular_50['Image-URL-M'].values),
                           votes=list(popular_50['Book-Rating'].values),
                           ratings=list(popular_50['avg_rating'].values),
                           name='PyCharm')

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html',name='PyCharm')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    book_loc = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(simillarity_score[book_loc])), key=lambda x: x[1], reverse=True)[1:6]
    suggestions = []
    for i in similar_items:
        item = []
        rec_filt = books['Book-Title'] == pt.index[i[0]]
        temp_df = books[rec_filt]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        suggestions.append(item)
    print(suggestions)
    return render_template('recommend.html',data=suggestions)


if __name__=='__main__':
    app.run(debug=True)