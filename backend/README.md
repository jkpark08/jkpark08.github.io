# Untact Makeup inference API

This folder wraps the original TensorFlow-v1/dlib implementation in a small Flask API for a static Jekyll project page.

## Important limitation

GitHub Pages/Jekyll can only host static HTML, CSS, JavaScript, and assets. It cannot execute `full_makeup.py`, TensorFlow, or dlib. The Python model must run on a separate server, while the project page sends image uploads to that server.

The public `jkpark0825/untact_makeup` repository exposes the inference scripts but the visible repository tree does **not** include the required `models/` checkpoint directory. This service expects these files before it can run:

```text
untact_makeup/
  full_makeup.py
  shape_predictor_68_face_landmarks.dat
  models/
    model.meta
    <matching TensorFlow checkpoint files>
```

## Local setup

Place this `backend/` directory next to a clone or copy of the original code:

```text
deployment/
  backend/
  untact_makeup/
```

Then run:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export UNTACT_MAKEUP_REPO="$(cd ../untact_makeup && pwd)"
export ALLOWED_ORIGINS="https://jkpark08.github.io"
python app.py
```

The server should be available at `http://localhost:7860`. Check model readiness with:

```bash
curl http://localhost:7860/health
```

## Docker deployment

Copy or mount the original `untact_makeup/` directory into this backend folder and run:

```bash
cd backend
docker compose up --build
```

The API endpoint is then:

```text
http://YOUR_SERVER:7860/api/makeup
```

Use HTTPS and a reverse proxy such as Nginx or Apache for public deployment. The Jekyll post expects the base URL only, for example `https://demo.example.com/untact-makeup`; it appends `/api/makeup` itself.

## API

`POST /api/makeup` accepts multipart form data:

- `source` — required source portrait
- `skin` — optional skin reference
- `lip` — optional lip reference
- `eye` — optional eye reference

The response body is a PNG image. Uploaded files are decoded in memory and reference images are only written to a temporary directory that is removed when the request completes.
