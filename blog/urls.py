from django.urls import path 
from blog.views import create_post,retrieve_post,update_post,delete_post,create_comment

urlpatterns=[
    path('create/',create_post),
    path('retrive/',retrieve_post),
    path('update/',update_post),
    path('delete/',delete_post),
    path('create_comment/',create_comment)

    

]