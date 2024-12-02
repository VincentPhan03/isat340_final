import cherrypy
import pymysql


def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Strongpassword123!',
        database='ctf',
        cursorclass=pymysql.cursors.DictCursor
    )


class CTFApp:
    @cherrypy.expose
    def index(self):
        return """
        <h1>Welcome to the CTF Platform</h1>
        <ul>
            <li><a href="/create_user">Create User</a></li>
            <li><a href="/create_challenge">Create Challenge</a></li>
            <li><a href="/leaderboard">View Leaderboard</a></li>
        </ul>
        """

    @cherrypy.expose
    def create_user(self, username=None, password=None, email=None):
        if cherrypy.request.method == 'POST':
            connection = get_db_connection()
            cursor = connection.cursor()

            try:
                cursor.execute(
                    "INSERT INTO users (username, password_hash, email) VALUES (%s, SHA2(%s, 256), %s)",
                    (username, password, email)
                )
                connection.commit()
                return "User created successfully!"
            except pymysql.MySQLError as e:
                return f"Error creating user: {e}"
            finally:
                connection.close()

        return """
        <h2>Create a New User</h2>
        <form method="POST" action="/create_user">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <input type="email" name="email" placeholder="Email" required><br>
            <button type="submit">Create User</button>
        </form>
        """

    @cherrypy.expose
    def create_challenge(self, title=None, description=None, points=None):
        if cherrypy.request.method == 'POST':
            connection = get_db_connection()
            cursor = connection.cursor()

            try:
                cursor.execute(
                    "INSERT INTO objectives (title, description, points) VALUES (%s, %s, %s)",
                    (title, description, points)
                )
                connection.commit()
                return "Challenge created successfully!"
            except pymysql.MySQLError as e:
                return f"Error creating challenge: {e}"
            finally:
                connection.close()

        return """
        <h2>Create a New Challenge</h2>
        <form method="POST" action="/create_challenge">
            <input type="text" name="title" placeholder="Challenge Title" required><br>
            <textarea name="description" placeholder="Challenge Description" required></textarea><br>
            <input type="number" name="points" placeholder="Points" required><br>
            <button type="submit">Create Challenge</button>
        </form>
        """

    @cherrypy.expose
    def leaderboard(self):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT u.username, o.title, l.completion_time, o.points
                FROM leaderboard l
                JOIN users u ON l.user_id = u.user_id
                JOIN objectives o ON l.objective_id = o.objective_id
                ORDER BY l.completion_time ASC
            """)
            results = cursor.fetchall()

            html = """
            <h2>Leaderboard</h2>
            <table border="1">
                <tr><th>Username</th><th>Challenge</th><th>Completion Time</th><th>Points</th></tr>
            """
            for row in results:
                html += f"<tr><td>{row['username']}</td><td>{row['title']}</td><td>{row['completion_time']}</td><td>{row['points']}</td></tr>"
            html += "</table>"

            return html
        except pymysql.MySQLError as e:
            return f"Error fetching leaderboard: {e}"
        finally:
            connection.close()


if __name__ == "__main__":
    cherrypy.config.update({
        'server.socket_port': 8080,
        'server.socket_host': '0.0.0.0',
        'tools.sessions.on': True
    })
    cherrypy.quickstart(CTFApp())
