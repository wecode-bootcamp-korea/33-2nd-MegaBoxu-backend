from datetime import datetime

from django.views import View
from django.http import JsonResponse
from django.db.models import Q

from .models import Region, MovieTheater

class RegionTheaterListView(View):
    def get(self, request):

        regions = Region.objects.all().prefetch_related("theater_set")

        region_theaters = [{
            'region_id'   : region.id,
            'region_name' : region.name,
            'theaters': [{
                'id'  : theater.id,
                'name': theater.name
                } for theater in region.theater_set.all()]
            } for region in regions]
        
        return JsonResponse({'region_theaters':region_theaters}, status=200)

class MovieTheaterView(View):
    def get(self, request):
        
        TODAY      = datetime.today().date()
        date       = request.GET.get('date', TODAY)
        movie_id   = request.GET.getlist('movie_id')
        theater_id = request.GET.getlist('theater_id')
        q          = Q()
                  
        if not theater_id:
            return JsonResponse({'MESSAGE':'THEATER_DOES_NOT_SELECTED'}, status=400)
        
        q.add(Q(start_time__date = date), q.AND)
        q.add(Q(theater_id__in = theater_id), q.AND)
        if movie_id:
            q.add(Q(movie_id__in = movie_id), q.AND)
        
        movie_theaters = MovieTheater.objects.filter(q).select_related('movie', 'theater').order_by('start_time')
        
        if not movie_theaters:
            return JsonResponse({'MESSAGE':'TIME_TABLE_DOES_NOT_EXIST'}, status=404)
        
        time_table = [
            {
                'movie_theater_id': movie_theater.id,
                'date'            : movie_theater.start_time.date(),
                'start_time'      : movie_theater.start_time.strftime("%H:%M"),
                'end_time'        : movie_theater.end_time,
                'movie_title'     : movie_theater.movie.title,
                'theater_name'    : movie_theater.theater.name
            } for movie_theater in movie_theaters]
        
        return JsonResponse({'time_table':time_table}, status=200)
