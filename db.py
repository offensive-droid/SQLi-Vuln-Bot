import sqlite3

# Connect to the database (create one if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create a table to store user data
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')

# Sample data to insert into the database
sample_data = [
    ('user1', 'password123'),
    ('user2', 'letmein'),
    ('user3', 'p@ssw0rd')
]

# Insert sample data into the database
cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', sample_data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created successfully with sample content.")
