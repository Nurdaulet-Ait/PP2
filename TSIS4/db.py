import psycopg2
from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("Database initialization error:", e)


def get_or_create_player(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    row = cur.fetchone()

    if row:
        player_id = row[0]
    else:
        cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
        player_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return player_id


def save_session(username, score, level):
    try:
        player_id = get_or_create_player(username)
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
            (player_id, score, level)
        )

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("Could not save result:", e)


def get_top_scores():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT p.username, gs.score, gs.level_reached, gs.played_at
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            ORDER BY gs.score DESC, gs.level_reached DESC, gs.played_at ASC
            LIMIT 10;
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    except Exception as e:
        print("Could not load leaderboard:", e)
        return []


def get_personal_best(username):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT COALESCE(MAX(gs.score), 0)
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            WHERE p.username = %s;
        """, (username,))

        best = cur.fetchone()[0]
        cur.close()
        conn.close()
        return best

    except Exception as e:
        print("Could not load personal best:", e)
        return 0
