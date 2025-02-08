import requests
import mysql.connector
import json

# Function to extract data from Sportradar API
def extract_data(api_url, headers):
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# Function to store data in MySQL database
def store_data(data, table_name, db_connection):
    cursor = db_connection.cursor()
    for item in data:
        columns = ', '.join(item.keys())
        values = ', '.join(['%s'] * len(item))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        cursor.execute(sql, list(item.values()))
    db_connection.commit()

# Main function
def main():
    api_url = "https://api.sportradar.com/tennis/trial/v3/en/competitions/sr%3Acompetition%3A3101/info.json?api_key=K5CF725694FlrfkZGMUX6K7WV8CeEbaYZKRTeNYb"
    headers = {
        "Accept": "application/json"
    }

    # Extract data
    data = extract_data(api_url, headers)

    # Print data to debug the structure
    print(data)

    if data and isinstance(data, list): # Check if data is a list
        # Connect to MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gsp@6090",
            database="sports_data"
        )
        
        # Store data
        store_data(data, "sports_data", db_connection)
        
        # Close the database connection
        db_connection.close()

if __name__ == "__main__":
    main()
