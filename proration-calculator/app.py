from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({"status": "running"})


@app.post("/charge")
def charge():
    data = request.get_json(force=True)

    old_price = data["old_price"]
    new_price = data["new_price"]
    days_remaining = data["days_remaining"]
    spec = data["spec"]

    if spec == "v1":
        divisor = 30
    else:
        divisor = data["days_in_actual_month"]

    result = (new_price - old_price) * (days_remaining / divisor)

    return jsonify({"charge": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
