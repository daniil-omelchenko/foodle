curl -X POST -d @webhook.json -H "Content-Type: application/json" "https://api.telegram.org/bot{token}/setWebhook"

gcloud appdeploy app.yaml --project foodle-219414 --version test

