import requests
from decouple import config
from .models import ProjectModel

def count_pull_requests(repo_name):
    pull_request_count = 0

    headers = {
        "accept": "application/vnd.github.v3+json",
    }

    response = requests.get(
        f"https://api.github.com/repos/Projectsv2/{repo_name}/issues",
        headers=headers,
        auth=("Abhiram-Joshi", config("GITHUB_ACCESS_TOKEN")),
    )

    if response.status_code == 200:
        response_json = response.json()

        for pr in response_json:
            if "pull_request" in pr:
                pull_request_count += 1

        instance = ProjectModel.objects.get(repo_name=repo_name)
        instance.repo_pull_requests = pull_request_count
        instance.save()

        return {"pull_request_count": pull_request_count, "status_code": response.status_code}
    
    else:
        return {"message":"Repository not found", "status_code":response.status_code}

def count_issues(repo_name):

    headers = {
        "accept": "application/vnd.github.v3+json",
    }

    response = requests.get(
        f"https://api.github.com/repos/Projectsv2/{repo_name}",
        headers=headers,
        auth=("Abhiram-Joshi", config("GITHUB_ACCESS_TOKEN")),
    )

    if response.status_code ==  200:

        response_json = response.json()
        issues_count = response_json["open_issues_count"]

        instance = ProjectModel.objects.get(repo_name=repo_name)
        instance.repo_issues = issues_count
        instance.save()

        return {"issues_count":issues_count, "status_code": response.status_code}

    else:
        return {"message":"Repository not found", "status_code":response.status_code}

def get_contributors(repo_name):

    contributor_count = 0

    headers = {
        "accept": "application/vnd.github.v3+json",
    }

    response = requests.get(
        f"https://api.github.com/repos/Projectsv2/{repo_name}/contributors",
        headers=headers,
        auth=("Abhiram-Joshi", config("GITHUB_ACCESS_TOKEN")),
    )

    if response.status_code == 200:
        response_json = response.json()

        response_contributors_list = []

        for contributor in response_json:

            response_contributor = {
                "username": contributor["login"],
                "profile_url": contributor["html_url"],
            }

            contributor_count += 1 

            response_contributors_list.append(response_contributor)
        
        return {
            "contributors":response_contributors_list,
            "contributors_count":contributor_count,
            "status_code": response.status_code
        }
    
    else:
        return {"message":"Repository not found", "status_code":response.status_code}


def get_languages(repo_name):

    headers = {
        "accept": "application/vnd.github.v3+json",
    }

    response = requests.get(
        f"https://api.github.com/repos/Projectsv2/{repo_name}/languages",
        headers=headers,
        auth=("Abhiram-Joshi", config("GITHUB_ACCESS_TOKEN")),
    )

    if response.status_code == 200:
        response_json = response.json()
        langs = [k for k,_ in response_json]

        instance = ProjectModel.objects.get(repo_name=repo_name)
        instance.repo_languages = langs
        instance.save()

        return {"languages":langs, "status_code": response.status_code}

    else:
        return {"message":"Repository not found", "status_code":response.status_code}