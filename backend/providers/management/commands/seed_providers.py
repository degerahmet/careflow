import datetime

from django.core.management.base import BaseCommand

from providers.models import ProviderAvailability, ProviderProfile
from users.models import User

SLOTS = [
    (datetime.time(9, 0), datetime.time(12, 0)),
    (datetime.time(13, 0), datetime.time(17, 0)),
]

PROVIDERS = [
    {
        "email": "dr.smith@careflow.dev",
        "first_name": "John",
        "last_name": "Smith",
        "specialty": "GEN",
        "bio": "Family medicine physician with 10 years of experience in primary care.",
    },
    {
        "email": "dr.johnson@careflow.dev",
        "first_name": "Sarah",
        "last_name": "Johnson",
        "specialty": "CARD",
        "bio": "Board-certified cardiologist specializing in preventive cardiology.",
    },
    {
        "email": "dr.patel@careflow.dev",
        "first_name": "Raj",
        "last_name": "Patel",
        "specialty": "DERMA",
        "bio": "Dermatologist focused on clinical and cosmetic skin care.",
    },
    {
        "email": "dr.chen@careflow.dev",
        "first_name": "Lisa",
        "last_name": "Chen",
        "specialty": "ENDO",
        "bio": "Endocrinologist treating diabetes, thyroid, and hormonal disorders.",
    },
    {
        "email": "dr.garcia@careflow.dev",
        "first_name": "Carlos",
        "last_name": "Garcia",
        "specialty": "GAST",
        "bio": "Gastroenterologist with expertise in digestive health and endoscopy.",
    },
    {
        "email": "dr.kim@careflow.dev",
        "first_name": "Mina",
        "last_name": "Kim",
        "specialty": "NEUR",
        "bio": "Neurologist specializing in headache disorders and epilepsy.",
    },
    {
        "email": "dr.brown@careflow.dev",
        "first_name": "Emily",
        "last_name": "Brown",
        "specialty": "PED",
        "bio": "Pediatrician dedicated to newborn and adolescent health.",
    },
    {
        "email": "dr.taylor@careflow.dev",
        "first_name": "Michael",
        "last_name": "Taylor",
        "specialty": "PSY",
        "bio": "Psychiatrist providing therapy and medication management for anxiety and depression.",
    },
    {
        "email": "dr.wilson@careflow.dev",
        "first_name": "Amanda",
        "last_name": "Wilson",
        "specialty": "RAD",
        "bio": "Diagnostic radiologist experienced in MRI, CT, and ultrasound imaging.",
    },
    {
        "email": "dr.lee@careflow.dev",
        "first_name": "David",
        "last_name": "Lee",
        "specialty": "SURG",
        "bio": "General surgeon with a focus on minimally invasive procedures.",
    },
]

DEFAULT_PASSWORD = "password123"


class Command(BaseCommand):
    help = "Seed provider users, profiles, and availabilities for local development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=len(PROVIDERS),
            help=f"Number of providers to create (max {len(PROVIDERS)}, default: all)",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=7,
            help="Number of weekdays of availability to generate per provider (default: 7)",
        )

    def handle(self, *args, **options):
        count = min(options["count"], len(PROVIDERS))
        days = options["days"]
        created_count = 0
        existing_count = 0
        slots_created = 0
        slots_existing = 0

        weekdays = self._next_weekdays(days)

        for data in PROVIDERS[:count]:
            user, created = User.objects.get_or_create(
                email=data["email"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "role": User.Role.PROVIDER,
                },
            )

            if created:
                user.set_password(DEFAULT_PASSWORD)
                user.save(update_fields=["password"])
                created_count += 1
            else:
                existing_count += 1

            # Profile is auto-created by post_save signal; just update fields.
            ProviderProfile.objects.filter(user=user).update(
                specialty=data["specialty"],
                bio=data["bio"],
            )

            profile = user.provider_profile
            for day in weekdays:
                for start, end in SLOTS:
                    _, slot_created = ProviderAvailability.objects.get_or_create(
                        provider=profile,
                        date=day,
                        start_time=start,
                        end_time=end,
                    )
                    if slot_created:
                        slots_created += 1
                    else:
                        slots_existing += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Providers: {created_count} created, {existing_count} existing. "
                f"Availability slots: {slots_created} created, {slots_existing} existing."
            )
        )

    @staticmethod
    def _next_weekdays(n):
        """Return the next `n` weekdays starting from today."""
        result = []
        day = datetime.date.today()
        while len(result) < n:
            if day.weekday() < 5:  # Mon-Fri
                result.append(day)
            day += datetime.timedelta(days=1)
        return result
