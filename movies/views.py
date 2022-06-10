from datetime import datetime

from django.views import View
from django.http import JsonResponse
from django.db.models import Q, Sum, Avg, Count

from .models import Movie, DailyViewer

class MovieListView(View):

    def get(self, request):
        
        sort   = request.GET.get("sort", None)
        offset = int(request.GET.get("offset", 0))
        limit  = int(request.GET.get("limit", 20))
        search = request.GET.get("search", None)
        q = Q()

        if sort == 'released':
            q.add(Q(release_date__lte=datetime.now().date()), q.AND)

        if search :
            q.add(Q(title__contains=search), q.AND)
             
        movies = Movie.objects.filter(q).order_by('-reservation_rate')[offset:limit]
        result = [{
            'movie_id'        : movie.id,
            'title'           : movie.title,
            'poster_url'      : movie.poster_url,
            'description'     : movie.description,
            'reservation_rate': movie.reservation_rate,
            'age_limit'       : movie.age_limit,
            'release_date'    : movie.release_date.strftime("%Y.%m.%d"),
        } for movie in movies]
        
        return JsonResponse({'result' : result}, status=200)

class MovieDetailView(View):

    def get(self, request):

        try:
            movie_id = request.GET.get("MovieNo")

            movie          = Movie.objects.get(id=movie_id)
            total_viewer   = movie.dailyviewer_set.all().aggregate(Sum('count'))
            avg_rating     = movie.review_set.all().aggregate(Avg('rating'))

            result = {
                'movie_id'        : movie.id,
                'title'           : movie.title,
                'poster_url'      : movie.poster_url,
                'movie_like_cnt'  : movie.movielike_set.count(),
                'review_cnt'      : movie.review_set.count(),
                'description'     : movie.description,
                'reservation_rate': movie.reservation_rate,
                'age_limit'       : movie.age_limit,
                'release_date'    : movie.release_date.strftime("%Y.%m.%d"),
                'average_rating'  : avg_rating['rating__avg'].normalize(),
                'total_viewer'    : total_viewer['count__sum'],
                'daily_viewers'   : [{
                    'date'  : viewer.date.strftime("%Y.%m.%d"),
                    'viewer': viewer.count
                } for viewer in movie.dailyviewer_set.all().order_by('-date')[:5]]
            }
            
            return JsonResponse({'result': result}, status=200)
        
        except Movie.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'MOVIE_DOES_NOT_EXIST'}, status=400)