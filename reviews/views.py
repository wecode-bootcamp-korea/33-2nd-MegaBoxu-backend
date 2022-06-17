import json, uuid, boto3

from django.http  import JsonResponse
from django.views import View

from users.models import User
from movies.models import Movie
from reviews.models import Review
from users.utils import login_decorator
from megaboxu.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

class MovieReviewView(View):

    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        )
    @login_decorator
    def post (self, request, movie_id):
        try:
            user      = request.user
            movie     = Movie.objects.get(id=movie_id)
            file      = request.FILES['image_url']
            file_uuid = str(uuid.uuid4())
            image_url = f"https://megaboxu-s3-bucket.s3.amazonaws.com/{file_uuid}"
            data      = request.POST
            content   = data['content']
            rating    = data['rating']
            self.s3_client.upload_fileobj(
                file,
                "megaboxu-s3-bucket",
                file_uuid,
                ExtraArgs = {
                    "ContentType" : file.content_type
                }
            )
            Review.objects.create(
                movie     = movie,
                image_url = image_url,
                user      = user,
                content   = content,
                rating    = rating
            )
            return JsonResponse({'message' : 'UPLOAD_SUCCESS', 'image_url' : image_url}, status=201)
            

        except KeyError:
            return JsonResponse({'message' : "KEY_ERROR"}, status=400)
        except Review.DoesNotExist:
            return JsonResponse({"message": "REVIEW_NOT_EXIST"}, status=404)

    @login_decorator
    def delete(self, request, movie_id):
        try:
            user      = request.user
            review_id = Review.objects.get(user_id = 23).delete()

            return JsonResponse({"message" : "DELETE_SUCCESS"}, status = 200)

        except Review.DoesNotExist:
            return JsonResponse({"message" : "CONTENT DOES NOT EXIST"}, status = 404)

    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie_id= movie_id)
        result  = [{
                  'id'        : review.id,
                  'user'      : review.user.name,
                  'image_url' : review.image_url,
                  'rating'    : review.rating,
                  'content'   : review.content,
                  'created_at': review.created_at.date()
            } for review in reviews]
    
        return JsonResponse({'review':result}, status=200)
