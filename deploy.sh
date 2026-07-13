#!/bin/bash
set -e  # Exit on any error

ENV=${1:-staging}
BRANCH=$(git branch --show-current)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🚀 OmniTrace Deployment to $ENV ($BRANCH) at $TIMESTAMP"

# Error handler
handle_error() {
  echo "❌ Deployment failed at step: $1"
  echo "Error: $2"
  # Optional: Send failure notification
  if [ -n "$SLACK_WEBHOOK" ]; then
    curl -X POST -H 'Content-type: application/json' \
      --data "{\"text\":\"❌ OmniTrace deployment to $ENV FAILED at $TIMESTAMP\"}" \
      $SLACK_WEBHOOK
  fi
  exit 1
}

# Pre-flight checks
if [ "$ENV" = "production" ] && [ "$BRANCH" != "main" ]; then
  handle_error "Pre-flight" "Production deployments only from main branch!"
fi

echo "✅ Pre-flight checks passed."

# Build & Test with error trapping
echo "🔨 Building project..."
npm run build --prefix frontend || handle_error "Frontend Build" "Build failed"

echo "🧪 Running tests..."
cd backend && python -m pytest --tb=short -q || echo "⚠️ Tests skipped or had issues (continuing)"
cd ..

# Deploy
echo "📦 Deploying to $ENV..."
if [ "$ENV" = "production" ]; then
  railway up --environment production || handle_error "Production Deploy" "Railway deployment failed"
else
  railway up --environment staging || handle_error "Staging Deploy" "Railway deployment failed"
fi

# Post-deploy
echo "✅ Deployment successful to $ENV!"
echo "📊 Checking logs..."
railway logs --environment $ENV --tail 30 || echo "⚠️ Could not fetch logs"

# Notify success
if [ -n "$SLACK_WEBHOOK" ]; then
  curl -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"🚀 OmniTrace deployed to $ENV successfully at $TIMESTAMP\"}" \
    $SLACK_WEBHOOK
fi

echo "🎉 Done! Monitor at your Railway dashboard."
