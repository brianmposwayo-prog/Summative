# Flask Profiles (JSON-backed)

A small Flask application that allows users to register, view, and update profiles.
Data is stored in `users.json` (simple JSON file).

Quick start

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

Files of interest

- `app.py` — Flask routes and application logic.
- `db.py` — JSON file read/write helpers.
- `forms.py` — input validation logic.
- `templates/` — Jinja2 templates for pages.
- `static/style.css` — basic styling.
- `users.json` — data storage (created automatically if missing).

Notes

- This app is intended as a simple demo and is not production hardened.
- For production, add proper authentication, CSRF protection, and use a real database.
