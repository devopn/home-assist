from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)


def save_state(state):
    with open(".current_state.json ", "w") as file:
        json.dump(state, file)


try:
    with open(".current_state.json ", "r") as file:
        actual_state = json.load(file)
except:
    with open(".current_state.json ", "w") as file:
        actual_state = {"temp": 0, "hum": 0, "color": "FFFFFF"}
        json.dump(actual_state, file)

@app.route("/")
def default():
    return {"it":"works"}

@app.route("/get_state")
def get_state():
    return actual_state

@app.route("/get_history", methods=["GET"])
def get_history():
    count = request.args.get("count")
    con = sqlite3.connect("/root/PROJECT/smart-home/home_sensors_log.sqlite")
    data = con.execute(
        """SELECT datetime, temp, hum FROM sensors ORDER BY id DESC LIMIT 0,?;""", (count,)
    ).fetchall()
    con.close()
    result = dict()
    for i in range(len(data)):
        result[i] = data[i]
    return jsonify(result)

@app.route("/set_state", methods=["POST"])
def set_state():
    data = request.json
    for i in data:
        if data[i] != -1:
            actual_state[i] = data[i]
    save_state(actual_state)

    con = sqlite3.connect("/root/PROJECT/smart-home/home_sensors_log.sqlite")
    cur = con.cursor()
    data = cur.execute(
        """INSERT INTO sensors(datetime, temp, hum) VALUES(datetime('now', '+180 minutes'), ?, ?)""", (actual_state['temp'], actual_state['hum'])
    )
    con.commit()
    con.close()

    return actual_state


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", debug=False)
    except:
        save_state(actual_state)
