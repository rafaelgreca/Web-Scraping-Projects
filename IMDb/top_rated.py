import requests
from bs4 import BeautifulSoup
import pandas as pd

#imdb top rated movies url
url = 'https://www.imdb.com/chart/top/'

def get_top_rated_movies():
    
    #csv columns
    columns = ['Ranking', 'Title', 'IMDb Rating']

    total_movies = []

    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    table = soup.find('table', {'class': 'chart'})

    #get the top rated movies tables
    table_body = table.find('tbody', {'class': 'lister-list'})

    #get all the rows from the table
    table_tr = table_body.findAll('tr')

    ranking = 1

    for tr in table_tr:

        movie = []

        #get the title
        td_title = tr.find('td', {'class': 'titleColumn'})
        td_title_a = td_title.find('a')

        #get the year
        td_title_span = td_title.find('span', {'class': 'secondaryInfo'})
        
        #get the imdb rating
        td_rating = tr.find('td', {'class': 'imdbRating'})
        td_rating_strong = td_rating.find('strong')

        #getting only the text
        title = td_title_a.get_text()
        year = td_title_span.get_text()

        title_year = title + ' ' + year
        imdb_rating = td_rating_strong.get_text()

        #infos about the movie
        movie.append(ranking)
        movie.append(title_year)
        movie.append(imdb_rating)

        #appending the movie in a list
        total_movies.append(movie)

        ranking += 1

    #creating the dataframe
    dataframe = pd.DataFrame(total_movies, columns=columns)

    #creating the csv file
    dataframe.to_csv('Top_Rated_Movies_IMDb.csv', index=False)

if __name__ == "__main__":
    get_top_rated_movies()