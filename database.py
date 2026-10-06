import sqlite3


DATABASE = "database.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            category TEXT NOT NULL,
            rating INTEGER NOT NULL,
            description TEXT,
            image_url TEXT,
            recommended_by TEXT
        )
    """)

    connection.commit()
    connection.close()

def get_recommendations(search="", category=""):
    connection = get_connection()

    query = "SELECT * FROM recommendations WHERE 1=1"
    values = []

    if search:
        query += " AND (name LIKE ? OR location LIKE ? OR description LIKE ?)"
        search_value = f"%{search}%"
        values.extend([search_value, search_value, search_value])

    if category:
        query += " AND category = ?"
        values.append(category)

    query += " ORDER BY id DESC"

    recommendations = connection.execute(
        query,
        values
    ).fetchall()

    connection.close()
    return recommendations



def add_recommendation(
    name,
    location,
    category,
    rating,
    description,
    image_url,
    recommended_by
):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO recommendations
        (
            name,
            location,
            category,
            rating,
            description,
            image_url,
            recommended_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            location,
            category,
            rating,
            description,
            image_url,
            recommended_by
        )
    )

    connection.commit()
    connection.close()

def get_recommendation_by_id(recommendation_id):
    connection = get_connection()

    recommendation = connection.execute(
        "SELECT * FROM recommendations WHERE id = ?",
        (recommendation_id,)
    ).fetchone()

    connection.close()
    return recommendation

def update_recommendation(
    recommendation_id,
    name,
    location,
    category,
    rating,
    description,
    image_url,
    recommended_by
):
    connection = get_connection()

    connection.execute(
        """
        UPDATE recommendations
        SET name = ?,
            location = ?,
            category = ?,
            rating = ?,
            description = ?,
            image_url = ?,
            recommended_by = ?
        WHERE id = ?
        """,
        (
            name,
            location,
            category,
            rating,
            description,
            image_url,
            recommended_by,
            recommendation_id
        )
    )

    connection.commit()
    connection.close()

def delete_recommendation(recommendation_id):
    connection = get_connection()

    connection.execute(
        "DELETE FROM recommendations WHERE id = ?",
        (recommendation_id,)
    )

    connection.commit()
    connection.close()
