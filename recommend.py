#using pandas for analyzing data
import pandas as pd
#importing sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
#for comparing matrix
from sklearn.metrics.pairwise import linear_kernel
import ast

#reads the .csv file and stores it in total
total = pd.read_csv('iCinDB11.csv', low_memory=False)
#stop_wd will remove the stop words from the plot
stop_wd = TfidfVectorizer(stop_words='english')
#fill any null plots with ''
total['overview'] = total['overview'].fillna('')
#movie_matrix will hold a matrix of movie plots
movie_matrix = stop_wd.fit_transform(total['overview'])
#will drop duplicates and keep the last occuring of each
indices = total['imdb_id'].reset_index().set_index('imdb_id')['index']
#compares two movie matrix
comp_matrix = linear_kernel(movie_matrix, movie_matrix)
#makes iterable dictionaries
total['crew'] = total['crew'].apply(lambda x: ast.literal_eval(x))
total['cast'] = total['cast'].apply(lambda x: ast.literal_eval(x))

class rec:
    def __init__(self):
        return None

    #finds different movies that director has directed
    def directorMovies(self, imdb):
        idx = indices[imdb]
        crew = total['crew'].iloc[idx]
        movies = []
        direct = ""
        for dic in crew:
            try:
                if dic['job'] == 'Director':
                    direct = dic['name']
            except:
                print("No director")
        if direct == "":
            direct = "No directs"
            return direct
            
        for row in total.iterrows():
            for column in row:
                if type(column) == int:
                    pass
                else:
                    for piece in column.iteritems():
                        if piece[0] == 'crew':
                            for dic in piece[1]:
                                try:
                                    if dic['job']=='Director':
                                        curr = dic['name']
                                except:
                                    pass
                                if curr == direct:
                                    for title in column.iteritems():
                                        if title[0] == 'title':
                                            if title[1] not in movies:
                                                movies.append(title[1])
        return movies

    #create a function to get the director of the movie
    def getDirector(self, title):
        idx = indices[title]
        crew = total['crew'].iloc[idx]
        direct = ""
        for dic in crew:
            try:
                if dic['job'] == 'Director':
                    direct = dic['name']
            except:
                print("No director")
        if direct == "":
            direct = "No director"
        return direct

    #create a function to get the first 3 actors who star in the movie
    def getActors(self, title):
        idx = indices[title]
        cast = total['cast'].iloc[idx]
        i=0
        stars = {}
        for dic in cast:
            stars[dic['name']] = dic['character']
            i+=1
            if i>=3:
                return stars

    #function to return one suggestion each for multiple movies
    def diff_compare_matrix(self, title_idx):
        score_list = list(enumerate(comp_matrix[title_idx]))
        score_list = sorted(score_list, key=lambda x: x[1], reverse=True)
        score_list = score_list[1:2]
        rec_title = [i[0] for i in score_list]
        for imdb in rec_title:
            name = total['title'].iloc[imdb]
            return name

    #function to return multiple movies suggestions for one title
    def compare_one(self, title_idx):
        score_list = list(enumerate(comp_matrix[title_idx]))
        score_list = sorted(score_list, key=lambda x: x[1], reverse=True)
        score_list = score_list[1:6]
        rec_titles = [i[0] for i in score_list]
        top = []
        for title in rec_titles:
            name = total['title'].iloc[title]
            top.append(name)
        return top

    #call this function to compare 5 movies, for 5 suggestions
    def diff_recommend(self, title1, title2, title3, title4, title5):
        title_list = [title1, title2, title3, title4, title5]
        top_rec = []
        for title in title_list:
            try:
                title_index = indices[title]
            except:
                print("Movie not found")
                top_rec.append("*** " + title)
            curr_top = self.diff_compare_matrix(title_index)
            top_rec.append(curr_top)
        return top_rec

    #call this function to get multiple suggestions for one movie
    def recommend_one(self, title):
        try:
            title_index = indices[title]
        except:
            print("Movie not found")
            return "Movie not found"
        top_movies = self.compare_one(title_index)
        return top_movies

title = title

title_index = indices[title]
score_list = list(enumerate(comp_matrix[title_idx]))
score_list = sorted(score_list, key=lambda x: x[1], reverse=True)
score_list = score_list[1:6]
rec_titles = [i[0] for i in score_list]
top = []
for title in rec_titles:
    name = total['title'].iloc[title]
    top.append(name)
print(top)