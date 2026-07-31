from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok"})

@app.route("/charge", methods=["POST"])
def charge():
    data = request.get_json(force=True)

    old_price = float(data["old_price"])
    new_price = float(data["new_price"])
    days_remaining = float(data["days_remaining"])
    days_in_actual_month = float(data["days_in_actual_month"])

    spec = str(data["spec"]).strip().lower()

    if spec == "v1":
        charge = (new_price - old_price) * (days_remaining / 30.0)
    elif spec == "v2":
        charge = (new_price - old_price) * (
            days_remaining / days_in_actual_month
        )
    else:
        return jsonify({"error": "invalid spec"}), 400

    return jsonify({"charge": round(charge, 10)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
