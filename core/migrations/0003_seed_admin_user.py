from django.db import migrations


def seed_admin(apps, schema_editor):
    User = apps.get_model("auth", "User")
    AllowedEmail = apps.get_model("core", "AllowedEmail")

    AllowedEmail.objects.get_or_create(email="admin@wovenry.com")

    if not User.objects.filter(username="admin").exists():
        user = User(
            username="admin",
            email="admin@wovenry.com",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password("admin123")
        user.save()


def unseed_admin(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username="admin").delete()
    AllowedEmail = apps.get_model("core", "AllowedEmail")
    AllowedEmail.objects.filter(email="admin@wovenry.com").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_seed_categories"),
    ]

    operations = [
        migrations.RunPython(seed_admin, unseed_admin),
    ]
