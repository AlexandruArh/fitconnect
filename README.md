# FitConnect MVP

> SWE6301 Agile Programming — Assessment 2  
> A web platform for organising fitness meetups and wellness events.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 4.2 (Python) |
| Database | Neon (PostgreSQL, serverless) |
| Frontend | Bootstrap 5 + Bootstrap Icons |
| Forms | django-crispy-forms |
| Hosting | Vercel |
| Static files | WhiteNoise |

## MVP Features

- ✅ User Registration & Login
- ✅ Event/Meetup Creation & Editing
- ✅ RSVP System (join / cancel)
- ✅ Dashboard showing upcoming sessions
- ✅ Category filtering (running, yoga, hiking, cycling, gym)

## Local Development Setup

```bash
# 1. Clone the repo
git clone https://github.com/AlexandruArh/fitconnect.git
cd fitconnect

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
copy .env.example .env
# Edit .env with your Neon DATABASE_URL and SECRET_KEY

# 5. Run migrations
python manage.py migrate

# 6. Create superuser (optional)
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
```

## Neon Database Setup

1. Go to [neon.tech](https://neon.tech) and create a free project
2. Create a database called `fitconnect`
3. Copy the **connection string** (with `?sslmode=require`)
4. Paste it as `DATABASE_URL` in your `.env` file

## Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Collect static files first
python manage.py collectstatic --noinput

# Deploy
vercel --prod
```

Add these environment variables in the Vercel dashboard:
- `SECRET_KEY`
- `DATABASE_URL` (Neon connection string)
- `DEBUG=False`
- `ALLOWED_HOSTS=.vercel.app`

## Running Tests

```bash
python manage.py test
```

## Project Structure

```
fitconnect/
├── fitconnect/          # Django project settings
├── accounts/            # User registration & login
├── events/              # Event CRUD + RSVP
├── dashboard/           # User dashboard
├── templates/           # HTML templates
├── static/css/          # Custom CSS
├── requirements.txt
├── vercel.json          # Vercel deployment config
└── manage.py
```
