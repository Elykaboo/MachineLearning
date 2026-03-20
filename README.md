# Retail Intelligence System (Next.js + Python API)

This project now uses a modular React frontend (Next.js + Tailwind CSS) and a Python FastAPI backend for ML predictions.

## Architecture

- Next.js app (`app/`, `components/`, `lib/`) provides the UI and Vercel-compatible frontend.
- Next API route (`app/api/predict/route.ts`) forwards prediction requests to Python backend.
- Python backend (`retail_api.py`) trains all 5 models and serves `/predict`.

## Local Run

1. Python backend:

```bash
cd /Users/kyleliwanag/Desktop/MachineLearning
source .venv/bin/activate
python -m pip install -r requirements.txt
python retail_api.py
```

2. Frontend:

```bash
cd /Users/kyleliwanag/Desktop/MachineLearning
cp .env.example .env.local
# set PYTHON_API_URL if needed (default: http://127.0.0.1:8000)
npm install
npm run dev
```

## Vercel Notes

- Deploy the Next.js frontend to Vercel.
- Deploy `retail_api.py` to a Python hosting service (Render/Railway/Fly/VM).
- Set `PYTHON_API_URL` in Vercel environment variables to the deployed backend URL.
- If using Render, follow [RENDER_DEPLOY.md](/Users/kyleliwanag/Desktop/MachineLearning/RENDER_DEPLOY.md) and the included [render.yaml](/Users/kyleliwanag/Desktop/MachineLearning/render.yaml) blueprint.
