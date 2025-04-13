import csv
import requests

# Define your Okta domain and API token
your_okta_domain = "<<your_okta_domain>>"
api_token = "<<your_api_token"

# Define the headers for the API request
headers = {"Authorization": f"SSWS {api_token}"}

# Function to get all apps from Okta with pagination
def get_all_apps():
    url = f"https://{your_okta_domain}/api/v1/apps"
    apps = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching apps: {response.status_code}")
            break
        data = response.json()
        apps.extend(data)
        url = response.links.get('next', {}).get('url')
    return apps

# Function to get app ID by app name
def get_app_id(app_name, apps):
    for app in apps:
        if app['label'] == app_name:
            return app['id']
    return None

# Read app names from CSV file and get app IDs
def read_csv_and_get_app_ids(csv_file_path):
    apps = get_all_apps()
    app_ids = {}
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            app_name = row[0]
            app_id = get_app_id(app_name, apps)
            if app_id:
                app_ids[app_name] = app_id
            else:
                app_ids[app_name] = "Not Found"
    return app_ids

# Example usage
csv_file_path = 'app_names.csv'
app_ids = read_csv_and_get_app_ids(csv_file_path)
for app_name, app_id in app_ids.items():
    print(f"App Name: {app_name}, App ID: {app_id}")
