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
    Todo(id=1, text="I'm a todo item"),
    Todo(id=2, text="Hi, that's another one"),
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

@app.get("/cal/<int:number>")
def show_square(number: int):
    result = number ** 2
    return render_template("cal.html", number=number, result=result)

@app.get("/image")
def image_form():
    # show form to input image URL
    return render_template("image.html")

@app.post("/image")
def image_post():
    # get image URL from form
    image_url = request.form.get("image_url", "").strip()
    if not image_url:
        return render_template("image.html", error="Please enter a valid image URL."), 400
    # render template to display image
    return render_template("image.html", image_url=image_url)

# --- BMI Calculator ---
def classify_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obesity"

@app.get("/bmi")
def bmi_form():
    # just render the form
    return render_template("bmi.html")

@app.post("/bmi")
def bmi_post():
    w = (request.form.get("weight") or "").strip()
    h = (request.form.get("height") or "").strip()

    # basic validation
    try:
        weight = float(w)
        height = float(h)
        assert weight > 0 and height > 0
    except Exception:
        return render_template("bmi.html", error="Please enter valid positive numbers."), 400
    if height > 10:  # if height is over 10, assume it's in cm
        height = height / 100
    bmi = round(weight / (height ** 2), 2)
    label = classify_bmi(bmi)
    return render_template("bmi.html",
                           weight=weight,
                           height=height,
                           bmi=bmi,
                           label=label)

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
