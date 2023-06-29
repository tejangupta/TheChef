from django.http import HttpResponse
from django.shortcuts import render
from itertools import combinations        # Use itertools to generate different combinations of elements
from youtube_search import YoutubeSearch  # Use to fetch YouTube top search results

# Will be used to concat with an input recipe
base = 'Cooking recipes only with'


def search(query):
    # Unwanted details fetched by api, so we will be using other results except elements in the remove
    remove = ['id', 'thumbnails', 'title', 'channel', 'duration', 'views', 'long_desc']

    # Use to fetch results of YouTube and max_results as 1, so we will be getting top results
    results = YoutubeSearch(query, max_results=1).to_dict()

    for result in results:
        # API will give the url without 'youtube.com' so we will be adding them manually
        result['url'] = 'https://www.youtube.com/' + result['url_suffix']

        # Except elements in 'remove'
        removed_items = [result.pop(key) for key in remove]

        return result


def index(request):
    return render(request, 'index.html')


def chef(request):
    # Retrieve text from user input in website
    text = request.POST.get('text', 'off')

    # As we use checkbox, so if user selected the option it will return 'true' or else 'false'
    small = request.POST.get('small', 'off')
    med = request.POST.get('med', 'off')
    large = request.POST.get('large', 'off')

    if small == 'on':
        print('small is clicked')
