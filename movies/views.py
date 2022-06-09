from datetime import datetime

from django.views import View
from django.http import JsonResponse
from django.db.models import Q

from .models import Movie

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