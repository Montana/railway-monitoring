## Railway Monitoring 

This script monitors the health and status of your Railway deployment instances. It performs connectivity checks against the Railway API, retrieves project information, and tests your deployment URLs to ensure everything is running smoothly.

## Getting Started

Before running the script, you need to install the requests library. You can do this by running pip install requests in your terminal. The script requires certain environment variables to function properly. You'll need to set `RAILWAY_TOKEN` with your Railway API token, `RAILWAY_PROJECT_ID` with your project identifier, and optionally `RAILWAY_DEPLOYMENT_URL` with the URL of your deployed application.

To get your Railway API token, log into your Railway dashboard and navigate to your account settings. You can generate a new token from the API tokens section. Your project ID can be found in the URL when viewing your project in the Railway dashboard, or you can retrieve it via the Railway CLI.

## Running the Script

The simplest way to run the script is to execute python railway_checker.py after setting your environment variables. If you prefer to specify the deployment URL directly, you can pass it as a command line argument like `python3 railway_checker.py https://your-app.railway.app`.

## Author
Michael Mendy (c) 2025.
