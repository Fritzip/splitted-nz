import json
from datetime import timedelta, datetime

from django.core.management.base import BaseCommand
from geodata.models import StravActivity

class Command(BaseCommand):
    args = '<jsonfile>'
    help = 'Create or update strava activities in database'

    def add_arguments(self, parser):
        parser.add_argument('jsonfile', nargs=1)

    def handle(self, *args, **options):
        with open(options["jsonfile"][0], encoding='utf8') as file:
            activities = json.load(file)
            for activity in activities:
                person, created = StravActivity.objects.update_or_create(
                        id=activity["id"], 
                        defaults={
                            "name": activity["name"],
                            "status" : activity["type"],
                            "average_speed" : activity["average_speed"],
                            "distance" : activity["distance"],
                            "elapsed_time" : activity["elapsed_time"],
                            "elev_high" : activity["elev_high"],
                            "elev_low" : activity["elev_low"],
                            "max_speed" : activity["max_speed"],
                            "moving_time" : timedelta(seconds=activity["moving_time"]),
                            "total_elevation_gain" : activity["total_elevation_gain"],
                            "start_date_local" : datetime.fromisoformat(activity["start_date_local"][:-1]),
                            "average_speed" : activity["average_speed"],
                            "polyline" : activity["map"]["summary_polyline"]
                        }
                )
                if created:
                    print("Created : {}".format(activity['name']))
                else:
                    print("Updated : {}".format(activity['name']))
