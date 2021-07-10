import requests
from decouple import config
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RepoModel

# Create your views here.


class ProjectDataAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        model_data = RepoModel.objects.all().values_list("url")
        data = []

        headers = {
            "accept": "application/vnd.github.v3+json",
        }

        i = 0
        for (url,) in model_data:

            response = requests.get(
                url,
                headers=headers,
                auth=("Abhiram-Joshi", config("GITHUB_ACCESS_TOKEN")),
            )

            response_json = response.json()

            data.append(dict())
            repo_data = data[i]


            # Name of repo
            repo_data["name"] = response_json["name"]


            # URL of repo
            repo_data["html_url"] = response_json["html_url"]


            # Number of issues of the repo
            repo_data["issues_count"] = response_json["open_issues_count"]


            # Readme content of repo
            readme_info = requests.get(
                f"{url}/contents/README.md",
                headers=headers,
                auth=("Abhiram-Joshi", config("GITHUB_ACCESS_TOKEN")),
            )

            readme_info_json = readme_info.json()

            repo_data["readme_content"] = readme_info_json["content"]


            # Contributors of a repository
            contributors = requests.get(
                f"{url}/contributors",
                headers=headers,
                auth=("Abhiram-Joshi", config("GITHUB_ACCESS_TOKEN")),
            )

            contributors_json = contributors.json()

            response_contributors_list = []

            for contributor in contributors_json:

                response_contributor = {
                    "name": contributor["login"],
                    "avatar_url": contributor["avatar_url"],
                    "profile_url": contributor["html_url"],
                }

                response_contributors_list.append(response_contributor)


            repo_data["contributors"] = response_contributors_list

            i += 1

        return Response(data)
