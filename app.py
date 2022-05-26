from flask import Flask
from flask import render_template, request
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=1de258408913c3801da46e5e75a8e7ea&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]
    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_genre = []
    recommended_movies_cast = []
    recommended_movies_overview = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_genre.append(movies.iloc[i[0]].genres)
        recommended_movies_cast.append(movies.iloc[i[0]].cast)
        recommended_movies_overview.append(movies.iloc[i[0]].overview)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_genre, recommended_movies_cast, recommended_movies_overview, recommended_movies_posters




movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def final():
    if request.method == "POST":
        selected_movie = request.form.get("fname")
        try:
            names, genre, cast, overview, posters = recommend(selected_movie)
        except:
            f = open(".\\templates\\index.html", "r")
            old_text = f.read()
            new_text = old_text.replace("Result", "<h7>Oops!!!<br>We could not find a match! Please try with other movie name.")
            return new_text
        x = " "
        y = " "
        j = 0
        for i in names:
            x = "<p><br clear = \"left\" ><img src=\"" + posters[j] + "\" align=\"right\" border = \"3px\" width=\"481\" height=\"721\"/><h2>" + i +"<br><br><h3>Genre:<h6>"+genre[j]+"<h3>Cast:<h6>"+cast[j]+"<h3>Overview:<h6>"+overview[j] +"<br><h3>Do you like this movie?&nbsp&nbsp<form action=\"/\" class=\"grid\" method=\"POST\"><input id=\"movie\" name=\"fname\" type=\"hidden\" value=\""+i+"\"/><br><button type=\"submit\"><img src=\"https://th.bing.com/th/id/OIP.MsthooL7A0ZSxg1fv8nglAHaHa?pid=ImgDet&rs=1\" height =\"50\" width=\"50\" alt=\"Like\"/></button></form>"+ "</p><br><br><br>"
            y = y + x
            j = j + 1
        y = y + " "
        f = open(".\\templates\\index.html", "r")
        old_text = f.read()
        new_text = old_text.replace("Result", y)
        return new_text
    return render_template('index.html')




if __name__ == '__main__':
    app.run()
