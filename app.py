from flask import Flask, render_template, request, redirect
import joblib
import requests
import os
from platform import python_version
from temp import api
print(python_version())

app = Flask(__name__)

print(os.getcwd())

new = joblib.load("E:\\neel_rec_sys\movie_list.pkl")
similarity = joblib.load("E:\\neel_rec_sys\similarity.pkl")
# os.getcwd() + "\similarity.pkl


def recommend(movie):
    # return ['a', 'b']
    index = new[new['title'] == movie].index[0]
    mli = []
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:6]:
        desc = new.iloc[i[0]].tags
        desc = (desc.split('.'))[0]
        mli.append([new.iloc[i[0]].title, api(
            new.iloc[i[0]].title), desc])
        # print(new.iloc[i[0]].tags)
    print(mli)

    return mli


@ app.route("/", methods=['GET', 'POST'])
def rec():
    print('Search pressed')
    if request.method == 'POST':
        print('post')
        n = request.form.get('movie')
        try:
            a = recommend(n)
        except:
            print(n)
            a = [[]]
        print(a)
        return render_template('index.html', movies=a)

    return render_template('index.html')


@ app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return rec()
    return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
