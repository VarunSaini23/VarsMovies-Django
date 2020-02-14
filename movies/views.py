from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.conf import settings
import datetime

from movies.models import Collection, Comment

TMDB_END_POINT = "https://api.themoviedb.org/3/"


# Create your views here.
def home(request):
    if request.method == 'POST':
        movie_name = request.POST.get('movie_name', None)
        if movie_name != '':

            movie_name = ''.join(movie_name.replace(" ", "_"))
            return redirect('search', movie_name)
        else:
            return redirect('home')
    else:
        endpoint = TMDB_END_POINT + "movie/top_rated?"
        params = {'api_key': settings.TMDB_API_KEY,
                  "language": 'en-US', 'page': 1}
        response = requests.get(endpoint, params=params)
        result = response.json()
        print("url : " + response.url)
        return render(request, "movies/home.html", {'results': result})


def upcoming(request):
    if request.method == 'POST':
        movie_name = request.POST.get('movie_name', None)
        return redirect('search', movie_name)
    else:
        endpoint = TMDB_END_POINT + "movie/upcoming?"
        params = {'api_key': settings.TMDB_API_KEY,
                  "language": 'en-US', 'page': 1}
        response = requests.get(endpoint, params=params)
        result = response.json()
        print("url : " + response.url)
        return render(request, "movies/home.html", {'results': result})


def popular(request):
    if request.method == 'POST':
        movie_name = request.POST.get('movie_name', None)
        return redirect('search', movie_name)
    else:
        endpoint = TMDB_END_POINT + "movie/popular?"
        params = {'api_key': settings.TMDB_API_KEY,
                  "language": 'en-US', 'page': 1}
        response = requests.get(endpoint, params=params)
        result = response.json()
        print("url : " + response.url)
        return render(request, "movies/home.html", {'results': result})


def search(request, query):
    if query != "":
        query = ''.join(query.replace("_", "%"))
        heading_query = ''.join(query.replace("%", " "))
        endpoint = TMDB_END_POINT + "search/movie?"
        params = {'api_key': settings.TMDB_API_KEY,
                  "language": 'en-US', 'page': 1, 'query': query}
        response = requests.get(endpoint, params=params)
        print(response.url)
        result = response.json()
        print("Heading query = " + heading_query)
        return render(request, 'movies/home.html', {'results': result, 'prev_query': heading_query})


def detail(request, movie_id):
    all_collection = []
    if request.user.is_authenticated:
        all_collection = request.user.collection_set.all()
    all_collection_movie_id_list = []
    for i in all_collection:
        all_collection_movie_id_list.append(i.movie_id)
    endpoint = TMDB_END_POINT + "movie/" + str(movie_id) + '?'
    endpoint_video = TMDB_END_POINT + "movie/" + str(movie_id) + '/video?'
    params = {'api_key': settings.TMDB_API_KEY, "language": 'en-US'}
    response = requests.get(endpoint, params=params)
    response_video = requests.get(endpoint_video, params=params)
    result = response.json()
    result_video = response_video.json()
    rel_date = result["release_date"]
    listDates = rel_date.split("-")
    x = datetime.datetime(int(listDates[0]), int(
        listDates[1]), int(listDates[2]))
    formatted_rel_date = x.strftime("%b %d %Y")
    comments = Comment.objects.filter(movie_id=movie_id)
    return render(request, 'movies/detail.html', {'results': result, 'formatted_rel_date': formatted_rel_date,
                                                  'result_video': result_video,
                                                  'all_collection_movie_id_list': all_collection_movie_id_list,
                                                  "comments": comments})


@login_required
def user_home_page(request, username):
    collections = Collection.objects.filter(user=request.user)
    results = []
    json_result = {}
    params = {'api_key': settings.TMDB_API_KEY, "language": 'en-US'}
    for i in range(len(collections)):
        endpoint = TMDB_END_POINT + "movie/" + \
            str(collections[i].movie_id) + '?'
        response = requests.get(endpoint, params=params)
        result = response.json()
        results.append(result)
    json_result['results'] = results
    print(json_result)

    return render(request, 'movies/user_home_page.html', {'json_result': json_result})


@login_required
def add_to_collection(request, movie_id):
    if request.method == "POST":
        user = request.user
        Collection.objects.create(user=user, movie_id=movie_id)
    return redirect('movie_detail', movie_id)


@login_required
def remove_from_collection(request, movie_id):
    if request.method == "POST":
        user = request.user
        Collection.objects.filter(user=user, movie_id=movie_id).delete()
    return redirect('movie_detail', movie_id)


@login_required
def add_comment(request, movie_id):
    if request.method == "POST":
        user = request.user
        Comment.objects.create(comment_text=request.POST.get(
            "comment_text"), uploaded_by=user, movie_id=movie_id)
    return redirect('movie_detail', movie_id)
