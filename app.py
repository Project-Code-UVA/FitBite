from flask import Flask, request, jsonify
import click
from db import get_db, close_db

def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = "database.db"

    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command():
        db = get_db()
        with open("schema.sql", "r") as f:
            db.executescript(f.read())
        db.commit()
        click.echo("Database initialized.")

    @app.post("/register")
    def register():
        db = get_db()
        username = request.json.get("username")
        email = request.json.get("email")

        db.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email)
        )
        db.commit()

        return jsonify({"message": "User registered!"}), 201

    return app
