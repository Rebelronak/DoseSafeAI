#!/bin/bash
# Simple script to trigger a Render deploy for a service.
# Usage: ./render_trigger.sh <service_id>

if [ -z "$1" ]; then
  echo "Usage: $0 <render_service_id>";
  exit 1;
fi

if [ -z "$RENDER_API_KEY" ]; then
  echo "Set RENDER_API_KEY environment variable.";
  exit 1;
fi

SERVICE_ID=$1

echo "Triggering deploy for Render service: $SERVICE_ID"

curl -X POST "https://api.render.com/v1/services/${SERVICE_ID}/deploys" \
  -H "Authorization: Bearer ${RENDER_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{}'

echo "Done."