import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host="localhost",     
        user="root",          
        password="Raj@77725", 
        database="job_database" 
    )
    return connection


def create_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Raj@77725"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS job_database")
    print("✅ Database 'job_database' is ready.")
    conn.close()


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            company VARCHAR(255),
            location VARCHAR(255),
            experience VARCHAR(100),
            skills TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Table 'jobs' is ready.")


def insert_jobs(jobs):
    conn = create_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO jobs (title, company, location, experience, skills)
        VALUES (%s, %s, %s, %s, %s)
    """

    for job in jobs:
        cursor.execute(insert_query, (
            job['title'],
            job['company'],
            job['location'],
            job['experience'],
            job['skills']
        ))

    conn.commit()
    conn.close()
    print(f"✅ Successfully inserted {len(jobs)} jobs into MySQL database.")
