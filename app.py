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
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Vincent's ISAT 340 Final Project</title>
        <!-- Bootstrap CSS -->
        <link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
        >
        </head>
        <body>
        <div class="container text-center mt-5">
            <h1>Welcome to Vincent's ISAT 340 Final Project!</h1>
            
            <!-- Navigation Bar -->
            <ul class="nav nav-pills nav-justified my-4">
            <li class="nav-item">
                <a class="nav-link" href="/create_user">Create User</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/create_challenge">Create Challenge</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/leaderboard">View Leaderboard</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/view_users">View All Users</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/view_challenges">View All Challenges</a>
            </li>
            </ul>
            
            <!-- Description -->
            <p class="lead">
            Explore the features of my ISAT 340 Final Project. Create new users, set up challenges, view the leaderboard, and browse all users and challenges.
            </p>
        </div>

        </body>
        </html>

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
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Create a New User</title>
            <!-- Bootstrap CSS -->
            <link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
            >
        </head>
        <body>
            <div class="container mt-5">
                <h2 class="text-center mb-4">Create a New User</h2>
                <form method="POST" action="/create_user" class="mx-auto" style="max-width: 400px;">
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input
                        type="text"
                        class="form-control"
                        id="username"
                        name="username"
                        placeholder="Enter username"
                        required
                        >
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input
                        type="password"
                        class="form-control"
                        id="password"
                        name="password"
                        placeholder="Enter password"
                        required
                        >
                    </div>
                    <div class="mb-4">
                        <label for="email" class="form-label">Email</label>
                        <input
                        type="email"
                        class="form-control"
                        id="email"
                        name="email"
                        placeholder="Enter email"
                        required
                        >
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Create User</button>
                </form> 
            </div>
            
        </body>
        </html>

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
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <title>Create a New Challenge</title>
            <!-- Bootstrap CSS -->
            <link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
            >
        </head>
        <body>
            <div class="container mt-5">
                <h2 class="text-center mb-4">Create a New Challenge</h2>
                <form method="POST" action="/create_challenge" class="mx-auto" style="max-width: 600px;">
                    <div class="mb-3">
                        <label for="title" class="form-label">Challenge Title</label>
                        <input
                        type="text"
                        class="form-control"
                        id="title"
                        name="title"
                        placeholder="Enter challenge title"
                        required
                        >
                    </div>
                    <div class="mb-3">
                        <label for="description" class="form-label">Challenge Description</label>
                        <textarea
                        class="form-control"
                        id="description"
                        name="description"
                        rows="5"
                        placeholder="Enter challenge description"
                        required
                        ></textarea>
                    </div>
                    <div class="mb-4">
                        <label for="points" class="form-label">Points</label>
                        <input
                        type="number"
                        class="form-control"
                        id="points"
                        name="points"
                        placeholder="Enter points for this challenge"
                        required
                        >
                    </div>
                    <button type="submit" class="btn btn-primary w-100 mb-3">Create Challenge</button>
                </form>
            </div>

        </body>
        </html>
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
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Leaderboard</title>
                <!-- Bootstrap CSS -->
                <link
                rel="stylesheet"
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
                >
            </head>
            <body>
                <div class="container mt-5">
                    <h2 class="text-center mb-4">Leaderboard</h2>
                    <table class="table table-striped table-bordered">
                        <thead class="table-dark">
                            <tr>
                                <th>Username</th>
                                <th>Challenge</th>
                                <th>Completion Time</th>
                                <th>Points</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>JohnDoe</td>
                                <td>Challenge 1</td>
                                <td>2023-10-12 14:30</td>
                                <td>100</td>
                            </tr>
                            <!-- Repeat <tr> for each entry -->
                        </tbody>
                    </table>
                    <a href="index" class="btn btn-secondary w-100">Back</a>
                </div>

            </body>
            </html>
            """
            for row in results:
                html += f"<tr><td>{row['username']}</td><td>{row['title']}</td><td>{row['completion_time']}</td><td>{row['points']}</td></tr>"
            html += "</table>"

            return html
        except pymysql.MySQLError as e:
            return f"Error fetching leaderboard: {e}"
        finally:
            connection.close()
            
    @cherrypy.expose
    def view_users(self):
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute("SELECT user_id, username, email, created_at FROM users")
            results = cursor.fetchall()

            html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>All Users</title>
                <!-- Bootstrap CSS -->
                <link
                rel="stylesheet"
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
                >
            </head>
            <body>
                <div class="container mt-5">
                    <h2 class="text-center mb-4">All Users</h2>
                    <table class="table table-striped table-bordered">
                        <thead class="table-dark">
                            <tr>
                                <th>User ID</th>
                                <th>Username</th>
                                <th>Email</th>
                                <th>Created At</th>
                            </tr>
                        </thead>
                        <tbody>
            """

            for row in results:
                html += f"""
                    <tr>
                        <td>{row['user_id']}</td>
                        <td>{row['username']}</td>
                        <td>{row['email']}</td>
                        <td>{row['created_at']}</td>
                    </tr>
            """

            html += """
                </tbody>
            </table>
            <!-- Back Button -->
            <a href="index" class="btn btn-secondary w-100">Back</a>
            </div>

            </body>
            </html>
            """

            return html
        except pymysql.MySQLError as e:
            return f"Error fetching users: {e}"
        finally:
            connection.close()


    @cherrypy.expose
    def view_challenges(self):
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute("SELECT objective_id, title, description, points, created_at FROM objectives")
            results = cursor.fetchall()

            html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>All Challenges</title>
        <!-- Bootstrap CSS -->
        <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
        >
    </head>
    <body>
        <div class="container mt-5">
            <h2 class="text-center mb-4">All Challenges</h2>
            <table class="table table-striped table-bordered">
                <thead class="table-dark">
                    <tr>
                        <th>Challenge ID</th>
                        <th>Title</th>
                        <th>Description</th>
                        <th>Points</th>
                        <th>Created At</th>
                    </tr>
                </thead>
                <tbody>
    """

            for row in results:
                html += f"""
                    <tr>
                        <td>{row['objective_id']}</td>
                        <td>{row['title']}</td>
                        <td>{row['description']}</td>
                        <td>{row['points']}</td>
                        <td>{row['created_at']}</td>
                    </tr>
    """

            html += """
                </tbody>
            </table>
            <!-- Back Button -->
            <a href="index" class="btn btn-secondary w-100">Back</a>
        </div>

    </body>
    </html>
    """

            return html
        except pymysql.MySQLError as e:
            return f"Error fetching challenges: {e}"
        finally:
            connection.close()


if __name__ == "__main__":
    cherrypy.config.update({
        'server.socket_port': 8080,
        'server.socket_host': '0.0.0.0',
        'tools.sessions.on': True
    })
    cherrypy.quickstart(CTFApp())
