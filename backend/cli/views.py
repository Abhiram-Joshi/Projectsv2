import re

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.models import ProjectModel

from . import utilities
from .serializers import CommandSerializer

# Create your views here.


class OrgCommandAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        if request.user.role == "admin":
            serializer = CommandSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            command = serializer.validated_data["command"]
            response = {}

            repo_name_pattern = re.compile(r"^create_repo (?P<name>\S+)")
            repo_name = re.match(repo_name_pattern, command).group("name")

            property_pattern = re.compile(
                r"(?P<property>--(?P<property_value>\w+) \S+)"
            )
            matches = re.findall(property_pattern, command)

            matches.sort(key=lambda a: a[1])

            command_sorted = f"create_repo {repo_name} "
            for match in matches:
                command_sorted += match[0] + " "

            create_repo_pattern = re.compile(
                (
                    r"^create_repo (?P<name>\S+)"
                    r"( --desc (?P<description>\S*))?"
                    r"( --gitignore (?P<gitignore_template>\S*))?"
                    r"( --home (?P<homepage>\S*))?"
                    r"( --license (?P<license_template>\S*))?"
                    r"( --vis (?P<visibility>\S*))?"
                )
            )

            if match := re.match(create_repo_pattern, command_sorted):
                try:
                    response = utilities.create_repo(match)
                    return Response(response, status=status.HTTP_201_CREATED)

                except:
                    import traceback
                    traceback.print_exc()
                    response = {"message": "Repository not created"}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)

            else:
                response = {"message": "Wrong command"}
                return Response(response, status=status.HTTP_404_NOT_FOUND)

        else:
            response = {"message": "User not authenticated"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):

        if request.user.role == "admin":
            serializer = CommandSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            command = serializer.validated_data["command"]
            response = {}

            delete_repo_pattern = re.compile(r"delete_repo (?P<repo_name>.+)")

            if match := re.match(delete_repo_pattern, command):
                response = utilities.delete_repo(match)

            if response:
                response = dict()
                response["message"] = "Repository deleted"
                try:
                    instance = ProjectModel.objects.get(repo_name=match.group("repo_name"))
                    contributor_instance = instance.repo_contributors.all()
                    contributor_instance.delete()
                    instance.delete()

                finally:
                    return Response(response, status=status.HTTP_202_ACCEPTED)

            else:
                response = dict()
                response["message"] = "Repository not found"
                return Response(response, status=status.HTTP_404_NOT_FOUND)

        else:
            response = {"message": "User not authenticated"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)


class DbCommandAPIView(APIView):

    def post(self, request):

        if request.user.role == "admin":
            serializer = CommandSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            command = serializer.validated_data["command"]
            response = {}

            add_project_pattern = re.compile(r"add_project (?P<repo_name>\S+)")

            if match:=re.match(add_project_pattern, command):
                response = utilities.add_project_to_db(match)

            
            if response["status_code"] == 200:
                return Response(response, status=status.HTTP_200_OK)

            else:
                return Response(response, status=status.HTTP_404_NOT_FOUND)

        else:
            response = {"message": "User not authenticated"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)


    def delete(self, request):
        
        if request.user.role == "admin":
            serializer = CommandSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            command = serializer.validated_data["command"]
            response = {}

            remove_project_pattern = re.compile(r"rem_project (?P<repo_name>\S+)")

            if match:=re.match(remove_project_pattern, command):
                response = utilities.remove_project_from_db(match)

            if response["status_code"] == 200:
                return Response(response, status=status.HTTP_200_OK)

            else:
                return Response(response, status=status.HTTP_404_NOT_FOUND)

        else:
            response = {"message": "User not authenticated"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)