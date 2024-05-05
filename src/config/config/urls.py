from django.contrib import admin
from django.urls import path
from issues.api import *  # noqa

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", get_issues),  # noqa
    path("issues/create-random", create_random_issue),  # noqa
    path("issues/post-issue", post_issue),  # noqa
    path("issues/create-issue", create_issue),  # noqa
    path("issues/<int:issue_id>", retreive_issue),  # noqa
]
