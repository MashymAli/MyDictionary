from multiprocessing import context
from django.shortcuts import render
from json_extract import GetValue2
import requests
from django.conf import settings

# Create your views here.

def index(request):
    return render(request,'index.html')

def search(request):

    if request.method == "POST":
        searched_word = request.POST['word']

        app_id  = settings.APP_ID
        app_key  = settings.SECRET_KEY
        language = "en-us"
        word_id = searched_word
        field1 = 'definitions'
        field2 = 'antonyms'
        field3 = 'synonyms'
        strictMatch = 'false'
        base_url='https://od-api.oxforddictionaries.com:443/api/v2/'

        url1 = base_url +'entries/' + language + '/' + word_id.lower() + '?fields=' + field1 + '&strictMatch=' + strictMatch
        url2 = base_url +'thesaurus/'+ language + '/' + word_id.lower() + '?fields=' + field2 + '&strictMatch=' + strictMatch
        url3 = base_url +'thesaurus/'+ language + '/' + word_id.lower() + '?fields=' + field3 + '&strictMatch=' + strictMatch
        result1 = requests.get(url1, headers = {"app_id": app_id, "app_key": app_key}).json()
        result2 = requests.get(url2, headers = {"app_id": app_id, "app_key": app_key}).json()
        result3 = requests.get(url3, headers = {"app_id": app_id, "app_key": app_key}).json()

        try:
            word = result1['results'][0]['id']
        except:
            word = "Invalid word"

        try:
            definition = result1['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions']
            definition = (', '.join(definition))
        except:
            definition = "No definition"

        try:
            final_antonyms = []
            
            getobj = GetValue2(result2)
            ant = getobj.get_values('antonyms')
            if len(ant) < 8:
                for items in ant:
                    final_antonyms.append(items['text']) 
                antonymsString = ','.join(final_antonyms)
            else:
                for x in range(8):
                    items = ant[x]
                    final_antonyms.append(items['text']) 
                antonymsString = ','.join(final_antonyms)

        except:
            antonymsString = "No antonyms"


        try:
            final_synonyms = []
            getobj2 = GetValue2(result3)
            syn = getobj2.get_values('synonyms')    #list
            if len(syn) < 8:   #if total synonyms in file is less than 10
                for items in syn:
                    final_synonyms.append(items['text']) 
                synonymsString = ','.join(final_synonyms)
            else:
                for x in range(8):    #print only 8 synonyms
                    items = syn[x]
                    final_synonyms.append(items['text']) 
                synonymsString = ','.join(final_synonyms)        
        except:
            synonymsString="No synonyms"

        context={
            'word': word,
            'Meaning': definition,
            'Synonyms':synonymsString,
            'Antonyms': antonymsString
        }
        return render(request,'index2.html',context)