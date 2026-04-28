# Wovenry

Django app for collecting, organizing, publishing, and remixing reusable metaprompts and prompt-backed projects.

## Local Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The app runs at `http://127.0.0.1:8000`.

## Configuration

Required environment:

```env
SECRET_KEY=change-me-to-a-random-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
GEMINI_API_KEY=your-gemini-api-key-here
DATABASE_URL=
```

Production deployments must set `SECRET_KEY`; the app refuses to boot with `DEBUG=False` and no secret key.

## Invite-Only Registration

Users can register only when their email exists in `AllowedEmail`. Add invites from the Django admin or shell:

```bash
python manage.py shell
```

```python
from core.models import AllowedEmail
AllowedEmail.objects.create(email="person@example.com")
```

Successful registration marks the invite as used.

## Deployment

Render uses `build.sh`, which installs dependencies, collects static files, and applies migrations. Create admin users through `createsuperuser` or the hosting console rather than seeding credentials in build scripts.

## Verification

```bash
python manage.py check
python manage.py test
```
