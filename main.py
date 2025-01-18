import requests
import mysql.connector

# Notion API setup
NOTION_API_KEY = "your_notion_api_key"
DATABASE_ID = "your_database_id"

# SQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="empathy_ledger"
)
cursor = conn.cursor()

# Fetch data from Notion
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28"
}
response = requests.post(url, headers=headers)
notion_data = response.json()["results"]

# Insert into SQL
for entry in notion_data:
    properties = entry["properties"]
    file_path = properties["File Path"]["url"] if "url" in properties["File Path"] else None
    description = properties["Description"]["rich_text"][0]["text"]["content"] if properties["Description"]["rich_text"] else None

    sql = """INSERT INTO media (file_path, description, created_at)
             VALUES (%s, %s, NOW
