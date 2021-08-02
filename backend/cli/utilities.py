import requests
from decouple import config
from project.models import ProjectModel
from django.core.exceptions import ObjectDoesNotExist
from project import utilities

def create_repo(match):
    name = match.group("name")
    visibility = match.group("visibility")
    description = match.group("description")
    gitignore_template = match.group("gitignore_template")
    license_template = match.group("license_template")

    headers = {
        "accept": "application/vnd.github.nebula-preview+json",
    }

    body = {
        "name": name,
        "visibility": visibility,
        "description": description,
        "auto_init": "true",
        "gitignore_template": gitignore_template,
        "license_template": license_template,
        "auto_init":"true",
    }

    body = {k: v for (k, v) in body.items() if v != None}

    response = requests.post(
        f"https://api.github.com/orgs/Projectsv2/repos",
        json=body,
        headers=headers,
        auth=("Abhiram-Joshi", config("GITHUB_ACCESS_TOKEN")),
    )

    response_json = response.json()

    instance = ProjectModel()
    instance.repo_name = response_json["name"]
    instance.repo_api_url = response_json["url"]
    instance.repo_html_url = response_json["html_url"]
    instance.repo_description = response_json["description"]
    instance.repo_languages = utilities.get_languages(response_json["name"])
    instance.repo_issues = utilities.count_issues(response_json["name"])
    instance.repo_pull_requests = utilities.count_pull_requests(response_json["name"])
    instance.save()

    return response_json


def delete_repo(match):
    repo_name = match.group("repo_name")

    response = requests.delete(
        f"https://api.github.com/repos/Projectsv2/{repo_name}",
        auth=("Abhiram-Joshi", config("GITHUB_ACCESS_TOKEN")),
    )

    json_response = response

    return json_response

def add_project_to_db(match):
    repo_name = match.group("repo_name")
    func_response = {}

    headers = {
        "accept": "application/vnd.github.nebula-preview+json",
    }

    response = requests.get(
        f"https://api.github.com/repos/Projectsv2/{repo_name}",
        headers=headers,
        auth=("Abhiram-Joshi", config("GITHUB_ACCESS_TOKEN")),
    )

    response_json = response.json()

    if response.status_code == 200 and not ProjectModel.objects.filter(repo_name=repo_name).exists():
        instance = ProjectModel()
        instance.repo_name = repo_name
        instance.repo_api_url = response_json["url"]
        instance.repo_html_url = response_json["html_url"]
        instance.repo_description = response_json["description"]
        instance.repo_languages = utilities.get_languages(repo_name)
        instance.repo_issues = utilities.count_issues(repo_name)
        instance.save()
        func_response["message"] = "Repository added"
        func_response["status_code"] = response.status_code

    else:
        func_response["message"] = "Repository could not be added"
        func_response["status_code"] = 404 if response.status_code==200 else response.status_code

    return func_response


def remove_project_from_db(match):
    repo_name = match.group("repo_name")
    response = {}

    try:
        instance = ProjectModel.objects.get(repo_name=repo_name)
        instance.delete()
        response["message"] = "Repository removed"
        response["status_code"] = 200

    except ObjectDoesNotExist:
        response["message"] = "Repository does not exist"
        response["status_code"] = 404
    
    finally:
        return response