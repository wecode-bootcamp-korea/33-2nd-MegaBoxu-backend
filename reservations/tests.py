from django.test import TestCase, Client

from .models import MovieTheater, Region, Theater
from movies.models import Movie

class RegionTheaterListViewTest(TestCase):

    def setUp(self):
        Region.objects.create(id = 1, name = "서울")
        Theater.objects.create(id = 1, name = "강남", region_id = 1)
        Theater.objects.create(id = 2, name = "강북", region_id = 1)

    def tearDown(self):
        Region.objects.all().delete()
        Theater.objects.all().delete()

    def test_success_get_region_theaters(self):
        client = Client()
        url = '/reservation/region-theater'
        response = client.get(url ,content_type='application/json')
        
        self.assertEqual(response.json(),{
            'region_theaters': [{
                'region_id'  : 1,
                'region_name': "서울",
                'theaters'   : [
                    {'id' : 1, 'name' : "강남"},
                    {'id' : 2, 'name' : "강북"}
                ]
            }]
        })

        self.assertEqual(response.status_code, 200)

class MovieTheaterViewTest(TestCase):
    
    def setUp(self):
        Movie.objects.create(
                id               = 1,
                title            = "브로커",
                poster_url       = "google.com",
                description      = "movie description 1",
                reservation_rate = 31.50,
                age_limit        = 12,
                release_date     = '2022-06-08',
                total_viewer     = 152364,
                running_time     = '01:30:00')
        
        Region.objects.create(id = 1, name = "서울")
        Theater.objects.create(id = 1, name = "강남", region_id = 1)

        MovieTheater.objects.create(id=1, movie_id=1, theater_id=1, start_time='2022-06-20 09:15:00')
        MovieTheater.objects.create(id=2, movie_id=1, theater_id=1, start_time='2022-06-20 11:30:00')
        
    def tearDown(self):
        Movie.objects.all().delete()
        Region.objects.all().delete()
        Theater.objects.all().delete()
        MovieTheater.objects.all().delete()

    def test_success_get_time_table(self):
        client = Client()
        url = '/reservation?date=2022-06-20&theater_id=1&movie_id=1'
        response = client.get(url ,content_type='application/json')

        self.assertEqual(response.json(), {
            'time_table' : [
                {
                    'movie_theater_id': 1,
                    "theater_name"    : "강남",
                    "movie_title"     : "브로커",
                    'date'            : "2022-06-20",
                    'start_time'      : "09:15",
                    'end_time'        : "10:45"
                },
                {
                    'movie_theater_id': 2,
                    "theater_name"    : "강남",
                    "movie_title"     : "브로커",
                    'date'            : "2022-06-20",
                    'start_time'      : "11:30",
                    'end_time'        : "13:00"
                }
            ]
        })
        self.assertEqual(response.status_code, 200)

    def test_theater_does_not_seleted_error(self):
        client = Client()
        url = '/reservation'
        response = client.get(url ,content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_time_table_does_not_exist_error(self):
        client = Client()
        url = '/reservation?theater_id=1'
        response = client.get(url ,content_type='application/json')

        self.assertEqual(response.status_code, 404)