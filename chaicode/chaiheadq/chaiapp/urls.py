from django.contrib import admin
from django.urls import path


from django.urls import path
from .views import Tweet_List, Tweet_create, Tweet_Edit, Tweet_Delete

urlpatterns = [
    path('', Tweet_List.as_view(), name="tweet_List"),
    path('tweet_create/', Tweet_create.as_view(), name="tweet_create"),
    path('tweet_edit/<int:id>/', Tweet_Edit.as_view(), name="tweet_edit"),  # Corrected here
    path('tweet_delete/<int:id>/', Tweet_Delete.as_view(), name="tweet_delete"),
]