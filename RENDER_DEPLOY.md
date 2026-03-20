# Render Deployment Guide (Python API)

## 1. Create Service

1. Open Render Dashboard.
2. Click **New +** -> **Blueprint**.
3. Select your repo: `Elykaboo/MachineLearning`.
4. Render will detect `render.yaml` and create:
   - `retail-intelligence-api` (Python web service)

## 2. Wait for Deploy

Render build/install and startup will run automatically.

Expected health endpoint:

`https://<your-service>.onrender.com/health`

It should return:

`{"status":"ok"}`

## 3. Use URL in Vercel

In Vercel project settings:

- Add environment variable:
  - `PYTHON_API_URL = https://<your-service>.onrender.com`

Then redeploy your Vercel app.

## 4. Verify End-to-End

- Open your Vercel app.
- Submit prediction form.
- Confirm all 5 model outputs are returned.
