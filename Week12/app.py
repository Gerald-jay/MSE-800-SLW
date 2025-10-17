from flask import Flask, render_template
from dataclasses import dataclass
from typing import List
from flask import Flask, render_template, request
from flask import jsonify, url_for, abort

app = Flask(__name__)

# Simple in-memory "database"
@dataclass
class Todo:
    id: int
    text: str

TODOS: List[Todo] = []  # Initially empty
TODOS = [
    Todo(id=1, text="Buy milk"),
    Todo(id=2, text="Read Python book")
]
_next_id = 3

@app.get("/")
def index():
    return render_template("index.html", todos=TODOS)

@app.get("/hello/<name>")
def hello(name: str):
    return render_template("hello.html", name=name)

@app.get("/echo")
def echo_form():
    return render_template("echo.html")

@app.post("/echo")
def echo_post():
    msg = request.form.get("message", "").strip()
    if not msg:
        return render_template("echo.html", error="Please type a message."), 400
    return render_template("echo.html", echoed=msg)

@app.get("/api/ping")
def api_ping():
    return jsonify({"status": "ok"})

def _new_id():
    global _next_id
    nid = _next_id
    _next_id += 1
    return nid

@app.get("/api/todos")
def api_todos():
    return jsonify([t.__dict__ for t in TODOS])

@app.post("/api/todos")
def api_create_todo():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "text is required"}), 400
    todo = Todo(id=_new_id(), text=text)
    TODOS.append(todo)
    return jsonify(todo.__dict__), 201, {"Location": url_for("api_get_todo", id=todo.id)}

@app.get("/api/todos/<int:id>")
def api_get_todo(id: int):
    for t in TODOS:
        if t.id == id:
            return jsonify(t.__dict__)
    abort(404)

@app.delete("/api/todos/<int:id>")
def api_delete_todo(id: int):
    global TODOS
    before = len(TODOS)
    TODOS = [t for t in TODOS if t.id != id]
    if len(TODOS) == before:
        abort(404)
    return "", 204

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)