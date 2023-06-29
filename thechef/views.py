from django.shortcuts import render
from itertools import combinations  # Use itertools to generate different combinations of elements
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

    pas = "You didn't select any operation " + '\n    or    \n' + \
          'User Should Provide Minimum Ingredients as Provided' \
          + '\n' + 'For Small Recipes:- at least 1\n' + 'For Medium Recipes:- at most 3\n' \
          + 'For Large Recipes:- at least 3\n' + 'THANK YOU'

    params = {'name': 'Error is', 'string': pas}

    ingredient_count = len(text.split(','))
    res1 = '\n CAUTION For Small Recipes:- At least 1 Ingredient\n'
    res2 = '\n CAUTION For Medium Recipes:- At most 3 Ingredients\n'
    res3 = '\n CAUTION For Large Recipes:- At least 3 Ingredients\n'

    if ingredient_count >= 1 and small == 'on':
        res1 = ''
        ingredients = text.split(',')

        for i in range(len(ingredients)):
            query = base + ' ' + ingredients[i]

            try:
                s = search(query)

                url = s['url']
                ss = url + ' ' + '(Ingredients Used : ' + ingredients[i] + ')'

                res1 = ss + '\n' + res1
            except Exception:
                continue

        res1 = 'These are the best Small/Quick recipes for your ingredients' + '\n' + res1
        params = {'name': '', 'string': str(res1 + '\n' + res2 + '\n' + res3)}

    if 3 >= ingredient_count >= 2 and med == 'on':
        res2 = ''
        ingredients = list(combinations(text.split(','), 2))

        for ingredient in ingredients:
            query = base + ' ' + ingredient[0] + ' and ' + ingredient[1]

            try:
                s = search(query)

                url = s['url']
                ss = url + ' ' + '(Ingredients Used : ' + ingredient[0] + ',' + ingredient[1] + ')'

                res2 = ss + '\n' + res2
            except Exception:
                continue

        res2 = 'These are the best Medium Recipes for your ingredients' + '\n' + res2
        params = {'name': '', 'string': str(res2 + '\n' + res1 + '\n' + res3)}

    if ingredient_count >= 3 and large == 'on':
        res3 = ''
        ingredients = text.split(",")

        if len(ingredients) > 3:
            ingredients = list(combinations(ingredients, 4))

            for ingredient in ingredients:
                if len(ingredients) <= 3:
                    query = base + ' ' + ingredient[0] + ' and ' + ingredient[1] + ' and ' + ingredient[2]

                    try:
                        s = search(query)
                        url = s['url']

                        ss = url + ' ' + '(Ingredients Used: ' + ingredient[0] + ',' + ingredient[1] + ' and ' + ingredient[2] + ')'
                        res3 = ss + '\n' + res3
                    except Exception:
                        continue

                    res3 = 'These are the best Large Recipes for your ingredients' + '\n' + res3
                    params = {'name': '', 'string': str(res3 + '\n' + res1 + '\n' + res2)}
                else:
                    query = base + ' ' + ingredient[0] + ' , ' + ingredient[1] + ' and ' + ingredient[2] + ' and ' + \
                            ingredient[3]

                    try:
                        s = search(query)
                        url = s['url']

                        ss = url + ' ' + '(Ingredients Used: ' + ingredient[0] + ',' + ingredient[1] + ' and ' + ingredient[2] + ')'
                        res3 = ss + '\n' + res3
                    except Exception:
                        continue

                    res3 = 'These are the best Large Recipes for your ingredients  : ' + '\n' + res3
                    params = {'name': '', 'string': str(res3 + '\n' + res1 + '\n' + res2)}
        else:
            ingredients = list(combinations(text.split(','), 3))

            for ingredient in ingredients:
                if len(ingredients) <= 3:
                    query = base + ' ' + ingredient[0] + ' and ' + ingredient[1] + ' and ' + ingredient[2]

                    try:
                        s = search(query)
                        url = s['url']

                        ss = url + ' ' + '(Ingredients Used: ' + ingredient[0] + ',' + ingredient[1] + ' and ' + ingredient[2] + ')'
                        res3 = ss + '\n' + res3
                    except Exception:
                        continue

                    res3 = 'These are the best Large Recipes for your ingredients  : ' + '\n' + res3
                    params = {'name': '', 'string': str(res3 + '\n' + res1 + '\n' + res2)}
                else:
                    query = base + ' ' + ingredient[0] + ' , ' + ingredient[1] + ' and ' + ingredient[2] + ' and ' + \
                            ingredient[3]
                    try:
                        s = search(query)
                        url = s['url']

                        ss = url + ' ' + '(Ingredients Used: ' + ingredient[0] + ',' + ingredient[1] + ' and ' + ingredient[2] + ')'
                        res3 = ss + '\n' + res3
                    except Exception:
                        continue

                    res3 = 'These are the best Large Recipes for your ingredients  : ' + '\n' + res3
                    params = {'name': '', 'string': str(res3 + '\n' + res1 + '\n' + res2)}

    return render(request, 'output.html', params)
