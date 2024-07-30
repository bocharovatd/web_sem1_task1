from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from app.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        # help = "Calculate popular_tags"
        popular_tags = Tag.objects.get_top()
        cache.set("popular_tags", popular_tags, 300)
