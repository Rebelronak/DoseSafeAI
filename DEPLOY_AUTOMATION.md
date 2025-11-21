Deployment automation

This repository contains GitHub Actions workflows and helper scripts to trigger automatic deployments for the frontend (Vercel) and backend (Render).

Required repository secrets (set these in GitHub -> Settings -> Secrets for this repository):
- `RENDER_API_KEY` - API key from your Render account with permissions to create deploys.
- `RENDER_SERVICE_ID` - The Render service ID for the backend service (found in Render service URL or settings).
- `VERCEL_TOKEN` - Personal token for Vercel.
- `VERCEL_PROJECT_ID` - Vercel project ID for the frontend.
- `VERCEL_ORG_ID` - Vercel organization ID (optional for some API calls).

How it works:
- Pushing to `main` triggers two workflows:
  - `.github/workflows/deploy-backend-render.yml` -> uses the Render API to POST a new deploy for your backend service.
  - `.github/workflows/deploy-frontend-vercel.yml` -> uses the Vercel API to create a deployment for the frontend.

Manual trigger:
- You can run `scripts/render_trigger.sh <render_service_id>` locally after exporting `RENDER_API_KEY`.

Notes:
- The GitHub Actions workflows only trigger deploys — they do not create services. Create the Render web service and the Vercel project manually in their respective dashboards first.
- For Render, configure the service's root directory as `backend`, the build command to `pip install -r requirements.txt` and the start command to `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2`.
- Set required env vars on Render: `GROQ_API_KEY`, any other secrets used by the backend.
- Set `VITE_API_URL` in Vercel to point to the Render backend URL after Render deploy is live.
