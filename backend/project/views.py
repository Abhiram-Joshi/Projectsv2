from decouple import config
import requests
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import ProjectModel
from .serializers import GetRepoSerializer, UploadImageSerializer
from . import utilities

# Create your views here.


class ProjectDataAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        # if request.user.role == "admin":

        model_data = ProjectModel.objects.values()
        field_names = [field.name for field in ProjectModel._meta.get_fields()]
        repo_field_names = list(filter(lambda s: s.startswith("repo"), field_names))
        repo_field_names.remove("repo_contributors")

        data = {}
        
        for instance_data in model_data:
            repo_data = dict()

            for i in repo_field_names:
                repo_data[i] = instance_data[i]

            response = requests.get(
                f"https://api.github.com/repos/{config('ORGANISATION')}/{instance_data['repo_name']}",
                headers = {"accept": "application/vnd.github.v3+json"},
                auth=("Abhiram-Joshi", config("GITHUB_ACCESS_TOKEN")),
            ).json()

            repo_data["stargazers_count"] = response["stargazers_count"]
            repo_data["repo_pull_requests"] = utilities.count_pull_requests(instance_data["repo_name"])["pull_request_count"]
            repo_data["repo_issues"] = response["open_issues_count"]
            repo_data["repo_forks"] = response["forks_count"]

            repo_data["repo_contributors"] = ProjectModel.objects.get(repo_name=instance_data["repo_name"]).repo_contributors.values()


            if data.get(repo_data["repo_creation_date"].year):
                data[repo_data["repo_creation_date"].year].append(repo_data)
            
            else:
                data[repo_data["repo_creation_date"].year] = [repo_data,]

        return Response(data, status=status.HTTP_200_OK)

        # else:
        #     response = {"message": "User not authenticated"}
        #     return Response(response, status=status.HTTP_403_FORBIDDEN)


class ProjectIssuesAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        # if request.user.role == "admin":
        serializer = GetRepoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        repo_name = serializer.validated_data["repo_name"]
        repo_data = dict()

        # Number of issues of the repo
        repo_data = utilities.count_issues(repo_name)

        return Response(repo_data, status=status.HTTP_200_OK)

        # else:
        #     response = {"message": "User not authenticated"}
        #     return Response(response, status=status.HTTP_403_FORBIDDEN)


class ProjectContributorsAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        
        # if request.user.role == "admin":
        serializer = GetRepoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        repo_name = serializer.validated_data["repo_name"]

        repo_data = utilities.get_contributors(repo_name)

        return Response(repo_data, status=status.HTTP_200_OK)

        # else:
        #     response = {"message": "User not authenticated"}
        #     return Response(response, status=status.HTTP_403_FORBIDDEN)


class ProjectLanguagesAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        # if request.user.role == "admin":
        serializer = GetRepoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        repo_name = serializer.validated_data["repo_name"]

        repo_data = utilities.get_languages(repo_name)

        return Response(repo_data, status=status.HTTP_200_OK)

        # else:
        #     response = {"message": "User not authenticated"}
        #     return Response(response, status=status.HTTP_403_FORBIDDEN)


class ProjectPullRequestsAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        
        # if request.user.role == "admin":
        serializer = GetRepoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        repo_name = serializer.validated_data["repo_name"]

        repo_data = utilities.count_pull_requests(repo_name)

        return Response(repo_data, status=status.HTTP_200_OK)

        # else:
        #     response = {"message": "User not authenticated"}
        #     return Response(response, status=status.HTTP_403_FORBIDDEN)


class ProjectYearAPIView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request):
        repo_data = {
            "data":[],
            "status_code":200
        }

        instance = ProjectModel.objects.values_list("repo_name", "repo_creation_date")

        for repo_name, repo_creation_date in instance:
            temp = dict()
            temp["repo_name"] = repo_name
            temp["repo_creation_year"] = repo_creation_date.year
            repo_data["data"].append(temp)

        return Response(repo_data, status=status.HTTP_200_OK)

class ProjectImageUploadAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UploadImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        repo_name = serializer.validated_data["repo_name"]
        base64_data = serializer.validated_data["repo_thumbnail"]

        try:
            instance = ProjectModel.objects.get(repo_name=repo_name)
            instance.repo_thumbnail = base64_data
            instance.save()

            return Response(
                {
                    "message":"success",
                    "status_code":200
                },
                status = status.HTTP_200_OK
            )
        
        except:
            return Response(
                {
                    "message":"Repository not found",
                    "status_code":404
                },
                status = status.HTTP_404_NOT_FOUND
            )