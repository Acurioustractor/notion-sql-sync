import requests
import mysql.connector

# Notion API setup
NOTION_API_KEY = "your_notion_api_key"  # Replace with your Notion API Key
DATABASE_ID = "your_database_id"  # Replace with your Notion Database ID

# SQL Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your SQL username
    password="YourNewPassword",  # Replace with your SQL password
    database="empathy_ledger"  # Replace with your SQL database name
)
cursor = conn.cursor()

# Fetch data from Notion
url = f"https://api.notion.com/v1/databases/{17cebcf981cf804a8e19e36a624d4dc4}/query"
headers = {
    "Authorization": f"Bearer {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}",
    "Notion-Version": "2022-06-28"
}
response = requests.post(url, headers=headers)
notion_data = response.json()["results"]

# Process and insert data into SQL
for entry in notion_data:
    properties = entry["properties"]

    # Extract fields from Notion (adjust field names based on your Notion structure)
    file_path = properties["File Path"]["url"] if "url" in properties["File Path"] else None
    description = properties["Description"]["rich_text"][0]["text"]["content"] if properties["Description"]["rich_text"] else None
    gallery_id = int(properties["Gallery"]["relation"][0]["id"]) if "relation" in properties["Gallery"] else None
    media_type = properties["Type"]["select"]["name"] if properties["Type"]["select"] else None

    # Insert into SQL database
    sql = """INSERT INTO media (file_path, description, gallery_id, type, created_at)
             VALUES (%s, %s, %s, %s, NOW())
             ON DUPLICATE KEY UPDATE description = %s, gallery_id = %s, type = %s"""
    cursor.execute(sql, (file_path, description, gallery_id, media_type, description, gallery_id, media_type
