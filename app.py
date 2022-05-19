from flask import Flask, render_template, request, jsonify
from recommend import rec
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
port = 5000
#app.run(host='0.0.0.0', port = 5000)

@app.route('/',methods=['POST'])
def main():
    #get the data from the json
    data = request.get_json()
    try:
        #get the array of imdb
        arr = data['imdb_ids']
    except:
        return "imdb_ids not found in data sent"
    newvar = rec()

    #use appropriate function based on if sent 1 or 5 imdb ids
    if(len(arr)==1):
        ids = newvar.recommend_one(arr[0])
        if ids == "Movie not found":
            return ids
        dic = {'imdb1':ids[0], 'imdb2':ids[1], 'imdb3':ids[2], 'imdb4':ids[3], 'imdb5':ids[4]}
        if ('director' in data):
            temp = newvar.getDirector(arr[0])
            if temp == "No director":
                dic['Director'] = "Not found"
            else:
                dic['Director'] = temp
        if('directs' in data):
            temp = newvar.directorMovies(arr[0])
            if temp == "No directs":
                dic['Directs:'] = "Not found"
            else:
                dic['Directs:'] = temp

    elif(len(arr)==5):
        ids = newvar.diff_recommend(arr[0],arr[1],arr[2],arr[3],arr[4])
        for i in range(5):
            found = ids[i]
            if found[:3] == "***":
                ids[i] = "***" + found[3:] + "not found"
        dic = {'imdb1':ids[0], 'imdb2':ids[1], 'imdb3':ids[2], 'imdb4':ids[3], 'imdb5':ids[4]}
        for i in range(5):
            directby = ['Director1', 'Director2', 'Director3', 'Director4','Director5']
            directs = ['Directs1','Directs2','Directs3','Directs4','Directs5']
            if ('director' in data):
                temp = newvar.getDirector(arr[i])
                dic[directby[i]] = temp
            if('directs' in data):
                temp = newvar.directorMovies(arr[i])
                dic[directs[i]] = temp
    else:
        return "Please enter either 1 or 5 imdb_id"

    #check if actors or directors were requested and if so add it to the dictionary to be returned
    if ('actors' in data):
        temp = newvar.getActors(arr[0])
        dic.update(temp)

    return dic

#api.add_resource(HelloWorld, '/fo')

if __name__ == '__main__':
    app.run(host='0.0.0.0')