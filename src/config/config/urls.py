from django.contrib import admin
from django.urls import path
from issues.api import (create_issue, create_poderevyanski_issue,
                        create_random_issue, get_issues,
                        get_poderevyanski_issue, post_issue, retreive_issue)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", get_issues),
    path("issues/create-random", create_random_issue),
    path("issues/oles", create_poderevyanski_issue),
    path("issues/get-oles", get_poderevyanski_issue),
    path("issues/post-issue", post_issue),
    path("issues/create-issue", create_issue),
    path("issues/<int:issue_id>", retreive_issue),
]
