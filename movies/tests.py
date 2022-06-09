from django.test import TestCase, Client

from .models import *

class MovieListViewTest(TestCase):
    
    def setUp(self):
        Movie.objects.bulk_create([
            Movie(
                id               = 1,
                title            = "브로커",
                poster_url       = "google.com",
                description      = "movie description 1",
                reservation_rate = 31.50,
                age_limit        = 12,
                release_date     = '2022-06-08',
                total_viewer     = 152364,
                running_time     = '01:01:00'
            ),
            Movie(
                id               = 2,
                title            = "범죄도시2",
                poster_url       = "naver.com",
                description      = "movie description 2",
                reservation_rate = 20.5,
                age_limit        = 15,
                release_date     = '2030-01-02',
                total_viewer     = 9575022,
                running_time     = '01:02:00'
            ),
            Movie(
                id               = 3,
                title            = "기라티나와 하늘의 꽃다발",
                poster_url       = "kakao.com",
                description      = "movie description 3",
                reservation_rate = 13.9,
                age_limit        = 0,
                release_date     = '2023-01-03',
                total_viewer     = 397784,
                running_time     = '01:03:00'
            )
        ])
    
    def tearDown(self):
        Movie.objects.all().delete()

    def test_success_movielist_get(self):
        
        client = Client()
        response = client.get('/movie')
        
        self.assertEqual(response.json(),
            {
                'result' : [
                    {
                        'movie_id'        : 1,
                        'title'           : "브로커",
                        'poster_url'      : "google.com",
                        'description'     : "movie description 1",
                        'reservation_rate': '31.50',
                        'age_limit'       : 12,
                        'release_date'    : "2022.06.08",
                    },
                    {
                        'movie_id'        : 2,
                        'title'           : "범죄도시2",
                        'poster_url'      : "naver.com",
                        'description'     : "movie description 2",
                        'reservation_rate': '20.50',
                        'age_limit'       : 15,
                        'release_date'    : "2030.01.02",
                    },
                    {
                        'movie_id'        : 3,
                        'title'           : "기라티나와 하늘의 꽃다발",
                        'poster_url'      : "kakao.com",
                        'description'     : "movie description 3",
                        'reservation_rate': '13.90',
                        'age_limit'       : 0,
                        'release_date'    : "2023.01.03",
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_success_movielist_filter_by_sort_realesed(self):

        client = Client()
        response = client.get('/movie?sort=released')

        self.assertEqual(response.json(),
            {
                'result' : [
                    {
                        'movie_id'        : 1,
                        'title'           : "브로커",
                        'poster_url'      : "google.com",
                        'description'     : "movie description 1",
                        'reservation_rate': '31.50',
                        'age_limit'       : 12,
                        'release_date'    : "2022.06.08",
                    },
                ]
            })
        self.assertEqual(response.status_code, 200)

    def test_success_movielist_filter_by_search(self):

        client = Client()
        response = client.get('/movie?search=하늘')

        self.assertEqual(response.json(),
            {
                'result' : [
                    {
                        'movie_id'        : 3,
                        'title'           : "기라티나와 하늘의 꽃다발",
                        'poster_url'      : "kakao.com",
                        'description'     : "movie description 3",
                        'reservation_rate': '13.90',
                        'age_limit'       : 0,
                        'release_date'    : "2023.01.03",
                    },
                ]
            })
        self.assertEqual(response.status_code, 200)