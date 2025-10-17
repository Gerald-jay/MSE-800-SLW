from app import app

def test_ping():
    client = app.test_client()
    r = client.get("/api/ping")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

def test_todo_crud():
    client = app.test_client()
    # create
    r = client.post("/api/todos", json={"text": "Read book"})
    assert r.status_code == 201
    tid = r.get_json()["id"]
    # list
    r = client.get("/api/todos")
    assert any(x["id"] == tid for x in r.get_json())
    # get single
    r = client.get(f"/api/todos/{tid}")
    assert r.status_code == 200
    # delete
    r = client.delete(f"/api/todos/{tid}")
    assert r.status_code == 204
    # ensure gone
    r = client.get(f"/api/todos/{tid}")
    assert r.status_code == 404

def test_cal_route():
    client = app.test_client()
    r = client.get("/cal/12")
    assert r.status_code == 200
    assert "The square of 12 is 144" in r.get_data(as_text=True)

def test_bmi_happy_path():
    client = app.test_client()
    r = client.post("/bmi", data={"weight": "68", "height": "1.73"})
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert "Your BMI is:" in html
    assert "Normal weight" in html

def test_bmi_invalid_input():
    client = app.test_client()
    r = client.post("/bmi", data={"weight": "-1", "height": "0"})
    assert r.status_code == 400
