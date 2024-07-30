from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from app.models import Profile


class Command(BaseCommand):
    def handle(self, *args, **options):
        # help = "Calculate best_members"
        best_members = Profile.objects.get_top()
        cache.set("best_members", best_members, 300)
