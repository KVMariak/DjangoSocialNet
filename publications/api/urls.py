from django.urls import path
from publications.api.views import (
    api_detail_post_view,
    api_update_post_view,
    api_delete_post_view,
    api_create_post_view,

    ApiPostListView
)

app_name = 'publications'

urlpatterns = [
    path('<slug>/', api_detail_post_view, name="detail"),
    path('<slug>/update', api_update_post_view, name="update"),
    path('<slug>/delete', api_delete_post_view, name="delete"),
    path('create', api_create_post_view, name="create"),
    path('list', ApiPostListView.as_view(), name="list"),
]
