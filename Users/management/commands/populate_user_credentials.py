from django.core.management.base import BaseCommand
from Users.models import UserCredentials
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = "Populate the database with 10 fixed user credentials"

    def handle(self, *args, **kwargs):
        user_data = [
            {"mobile": "9876543210", "password": "password123"},
            {"mobile": "8765432109", "password": "securepass456"},
            {"mobile": "7654321098", "password": "pass789"},
            {"mobile": "6543210987", "password": "randomPass321"},
            {"mobile": "5432109876", "password": "testPassword987"},
            {"mobile": "4321098765", "password": "mypassword001"},
            {"mobile": "3210987654", "password": "qwerty123"},
            {"mobile": "2109876543", "password": "helloWorld999"},
            {"mobile": "1098765432", "password": "admin2024"},
            {"mobile": "1987654321", "password": "letmein555"}
        ]

        for data in user_data:
            UserCredentials.objects.get_or_create(mobile=data["mobile"], defaults={"password": data["password"]})

        self.stdout.write(self.style.SUCCESS("10 fixed user credentials added successfully!"))