# Lora Real Estate – Render Deployment

## Quick Setup

1. **Create a Web Service** on [Render](https://render.com)
2. Connect your GitHub repo
3. Use these settings:

| Setting | Value |
|--------|-------|
| **Root Directory** | `backend` |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput` |
| **Start Command** | `gunicorn config.wsgi:application` |
| **Python Version** | 3.12 (set in Render dashboard or add `runtime.txt` with `python-3.12.0`) |

## Environment Variables

| Variable | Required | Notes |
|----------|----------|-------|
| `SECRET_KEY` | Yes | Use a long random string (e.g. from `python -c "import secrets; print(secrets.token_urlsafe(50))"`) |
| `DATABASE_URL` | Yes | From Render Postgres, or your own Postgres connection string |
| `RENDER_EXTERNAL_HOSTNAME` | Auto | Set automatically by Render for web services |
| `CLOUDINARY_URL` | No | For image uploads (or use `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`) |

## Post-Deploy: Create Admin User

After first deploy with a new database:

```bash
# Run in Render shell or locally with DATABASE_URL
cd backend
python manage.py ensure_admin
# Uses default: username lora / password lora@25 (change after first login)
```

## Admin Login

- **URL:** `https://your-app.onrender.com/admin/`
- **Default:** username `lora`, password `lora@25`

## Troubleshooting

- **500 Error:** Check Render logs. Common causes: missing `SECRET_KEY`, `DATABASE_URL`, or migrations.
- **Static files missing:** Ensure `collectstatic` runs in the build command.
- **Login redirect fails:** Ensure `RENDER_EXTERNAL_HOSTNAME` (or `ALLOWED_HOSTS`) includes your Render URL.
