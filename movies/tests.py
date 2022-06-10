from urllib import response
from django.test import TestCase, Client

from .models import *
from users.models import *
from reviews.models import *

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

class MovieDetailViewTest(TestCase):
    
    def setUp(self):
        Movie.objects.create(
            id               = 1,
            title            = "브로커",
            poster_url       = "https://img.megabox.co.kr/SharedImg/2022/05/12/y1RvPjCDEgjkIG2fbquiF4Tnm7zNIoJT_420.jpg",
            description      = "movie description 1",
            reservation_rate = 37.20,
            age_limit        = 12,
            release_date     = '2022-06-08',
            total_viewer     = 152364,
            running_time     = '01:01:00'
        )

        DailyViewer.objects.bulk_create([
            DailyViewer(id = 1, date = "2022-05-31", count = 2240, movie_id = 1),
            DailyViewer(id = 2, date = "2022-06-02", count = 3343, movie_id = 1),
            DailyViewer(id = 3, date = "2022-06-03", count = 560, movie_id = 1),
            DailyViewer(id = 4, date = "2022-06-08", count = 146221, movie_id = 1)
        ])

        User.objects.bulk_create([
            User(id = 1, kakao_id = "test1", email = "test1@test.com", name = "테스트1", phone_number = "01000010001", point = 50000),
            User(id = 2, kakao_id = "test2", email = "test2@test.com", name = "테스트2", phone_number = "01000020002", point = 100000)
        ])
        
        Review.objects.bulk_create([
            Review(id = 1, content = "review 1", rating = 10, image_url = "google.com", movie_id = 1, user_id = 1),
            Review(id = 2, content = "review 3", rating = 5, image_url = "naver.com", movie_id = 1, user_id = 2),
        ])

        MovieLike.objects.bulk_create([
            MovieLike(id = 1, movie_id =1, user_id = 1),
            MovieLike(id = 2, movie_id =1, user_id = 2),
        ])

    def tearDown(self):
        Movie.objects.all().delete()
        User.objects.all().delete()
        Review.objects.all().delete()
        MovieLike.objects.all().delete()

    def test_success_moviedetail_get(self):
        client   = Client()
        response = client.get('/movie/detail?MovieNo=1')
        
        self.assertEqual(response.json(), 
            {
                'result': {
                    "movie_id": 1,
                    "title": "브로커",
                    "poster_url": "https://img.megabox.co.kr/SharedImg/2022/05/12/y1RvPjCDEgjkIG2fbquiF4Tnm7zNIoJT_420.jpg",
                    "movie_like_cnt": 2,
                    "review_cnt": 2,
                    "description": "movie description 1",
                    "reservation_rate": "37.20",
                    "age_limit": 12,
                    "release_date": '2022.06.08',
                    "average_rating": "7.5",
                    "total_viewer": 152364,
                    "daily_viewers": [
                        {
                            "date": "2022.06.08",
                            "viewer": 146221
                        },
                        {
                            "date": "2022.06.03",
                            "viewer": 560
                        },
                        {
                            "date": "2022.06.02",
                            "viewer": 3343
                        },
                        {
                            "date": "2022.05.31",
                            "viewer": 2240
                        }
                    ]
                }
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_fail_moviedetail_get_doesnotexist(self):
        client = Client()
        response = client.get('/movie/detail?MovieNo=3')

        self.assertEqual(response.json(), {'MESSAGE' : 'MOVIE_DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 400)
