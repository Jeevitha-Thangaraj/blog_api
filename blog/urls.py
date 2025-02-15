from django.urls import path 
from blog.views import create_post,retrieve_post,update_post,delete_post,create_comment,read_comment,update_comment,delete_comment,list_comments

urlpatterns=[
    path('create/',create_post),
    path('retrive/',retrieve_post),
    path('update/',update_post),
    path('delete/',delete_post),
    path('create_comment/',create_comment),
    path('comments/<int:comment_id>/', read_comment),
    path('comments/<int:comment_id>/update/', update_comment),
    path('comments/<int:comment_id>/delete/', delete_comment),
    path('comments/list-comments/',list_comments),



]