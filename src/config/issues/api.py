# Create your views here.
import json
import random
import string

from django.http import HttpRequest, JsonResponse
from issues.models import Issue


def get_issues(request: HttpRequest) -> JsonResponse:
    if request.method != "GET":
        raise Exception("Only GET method is allowed")

    issues: list[Issue] = Issue.objects.all()

    results: list[dict] = [
        {
            "id": issue.id,
            "title": issue.title,
            "body": issue.body,
            "senior_id": issue.senior_id,
            "junior_id": issue.junior_id,
        }
        for issue in issues
    ]

    return JsonResponse(data={"results": results})


def _random_string(length: int = 10) -> str:
    return "".join([random.choice(string.ascii_letters) for i in range(length)])  # noqa


def create_random_issue(request: HttpRequest) -> JsonResponse:
    issue = Issue.objects.create(
        title=_random_string(20),
        body=_random_string(30),
        senior_id=1,
        junior_id=2,
    )

    result = {
        "id": issue.id,
        "title": issue.title,
        "body": issue.body,
        "senior_id": issue.senior_id,
        "junior_id": issue.junior_id,
    }

    return JsonResponse(data=result)


def create_my_post_issue(request: HttpRequest) -> JsonResponse:

    post_data = json.loads(request.body)

    issue = Issue.objects.create(
        title=post_data.get("title"),
        body=post_data.get("body"),
        senior_id=post_data.get("senior_id"),
        junior_id=post_data.get("junior_id"),
    )

    result = {
        "id": issue.id,
        "title": issue.title,
        "body": issue.body,
        "senior_id": issue.senior_id,
        "junior_id": issue.junior_id,
    }

    return JsonResponse(data=result)
