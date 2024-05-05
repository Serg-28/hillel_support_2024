import json
import random
import string

from django.http import Http404  # noqa
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render  # noqa
from django.shortcuts import get_object_or_404
from issues.models import Issue
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"


@api_view()
def get_issues(request) -> Response:

    issues = Issue.objects.all()
    # results = [IssueSerializer(issue) for issue in issues]
    results = [IssueSerializer(issue).data for issue in issues]

    return Response(data={"results": results})


@api_view()
def retreive_issue(request, issue_id: int) -> Response:
    instance = get_object_or_404(Issue, id=issue_id)
    return Response(data={"results": IssueSerializer(instance).data})


@api_view(["POST"])
def create_issue(request) -> Response:
    try:
        payload: dict = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        raise Exception("Request body is invalid")

    serializer = IssueSerializer(data=payload)
    serializer.is_valid(raise_exception=True)

    issue = Issue.objects.create(**serializer.validated_data)
    return Response(data=IssueSerializer(issue).data)


def _random_string(length: int = 10) -> str:
    return "".join(random.choice(string.ascii_letters) for i in range(length))


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


def post_issue(request: HttpRequest) -> JsonResponse:
    post_data = json.loads(request.body)

    issues = Issue.objects.create(
        title=post_data.get("title"),
        body=post_data.get("body"),
        senior_id=post_data.get("senior_id"),
        junior_id=post_data.get("junior_id"),
    )

    result = {
        "title": issues.title,
        "body": issues.body,
        "senior_id": issues.senior_id,
        "junior_id": issues.junior_id,
    }

    return JsonResponse(data=result)
