import random
from datetime import timedelta
from types import SimpleNamespace
from zoneinfo import ZoneInfo

from django.apps import apps
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker

fake = Faker()

MODE_FIXED = "fixed"
MODE_RANDOM = "random"
MODE_CLEAR = "clear"

BANNERS_DIR = settings.MEDIA_ROOT / "debug/seed_images"

class Command(BaseCommand):
    help = "Seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--mode",
            type=str,
            choices=[MODE_FIXED, MODE_RANDOM, MODE_CLEAR],
            default=MODE_FIXED,
            help="Mode: 'fixed' (create with fixed data), 'random' (create with random data) or 'clear' (only clear)",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=15,
            help="Number of records to create (only in random mode)",
        )

    def handle(self, *args, **options):
        mode = options["mode"]
        count = options["count"]

        self.stdout.write(f"Seeding data in {mode} mode...")
        run_seed(self, mode, count)
        self.stdout.write(self.style.SUCCESS("Done."))


def clear_data(models):
    for name, model in vars(models).items():
        if name.lower() == "user":
            # Delete all users except superusers
            model.objects.exclude(is_superuser=True).delete()
        else:
            model.objects.all().delete()


def create_fixed_organizations(models):
    return [
        models.Organization(
            title="University of Toronto Mississauga",
            slug="utm",
            description=fake.text(max_nb_chars=400),
            background=fake.text(max_nb_chars=400),
        ),
        models.Organization(
            title="Queens University",
            slug="queens",
            description=fake.text(max_nb_chars=400),
            background=fake.text(max_nb_chars=400),
        ),
    ]


def random_banner():
    images = []

    if not BANNERS_DIR.exists():
        return None

    for ext in ("*.png", "*.jpg"):
        images.extend(BANNERS_DIR.glob(ext))

    if not images:
        return None

    img_path = random.choice(images)  # noqa: S311
    return File(open(img_path, "rb"))  # noqa: PTH123


def create_fixed_users(models):
    return [
        models.User(
            username="fixeduser1",
            email="fixeduser1@example.com",
            password="password123",  # noqa: S106
        ),
        models.User(
            username="fixeduser2",
            email="fixeduser2@example.com",
            password="password123",  # noqa: S106
        ),
    ]

def create_random_posts(models, count=15):
    start_date = fake.date_time_this_year(tzinfo=ZoneInfo(settings.TIME_ZONE))
    end_date = start_date + timedelta(days=1)

    return [
        models.Post(
            title=fake.sentence(),
            description=fake.text(max_nb_chars=400),
            organization=models.Organization.objects.first(),
            author=models.User.objects.order_by("?").first(),
            start_date=start_date,
            end_date=end_date,
            location=f"{fake.city()}, {fake.country()}",
            tags=",".join(fake.words(nb=3)),
            image=random_banner(),
        ) for _ in range(count)
    ]


def run_seed(command, mode, count):
    """Seed database based on mode"""
    models = SimpleNamespace(
        Post=apps.get_model("posts", "Post"),
        Organization=apps.get_model("organizations", "Organization"),
        User=apps.get_model("users", "User"),
    )

    if mode == MODE_CLEAR:
        clear_data(models)
        command.stdout.write("Cleared all data.")
        return


    if mode == MODE_FIXED:
        clear_data(models)
        command.stdout.write("Cleared all data before fixed initialization.")

        seed_factories = [
            ("organization", create_fixed_organizations, models),
            ("user", create_fixed_users, models),
            ("post", create_random_posts, models, count),
        ]

    for key, factory, *args in seed_factories:
        command.stdout.write(f"Creating {key}{'s' if key[-1] == 's' else ''}...")
        for obj in factory(*args) or []:
            obj.save()
            command.stdout.write(f"Created {key}: {obj!s}")
