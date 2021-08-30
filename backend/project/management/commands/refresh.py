from django.core.management.base import BaseCommand, CommandError
from project.models import ProjectModel
from project import utilities

class Command(BaseCommand):
    help = "Refreshes data in the database"

    def add_arguments(self, parser):
        parser.add_argument('refresh', nargs="?", type=str)

    def handle(self, **options):
        repo_names = ProjectModel.objects.values_list("repo_name", flat=True)
        for repo_name in repo_names:
            for i in dir(utilities):
                item = getattr(utilities, i)
                if callable(item):
                    try:
                        item(repo_name)
                    except:
                        pass