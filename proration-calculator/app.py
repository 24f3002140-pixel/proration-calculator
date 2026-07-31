from decimal import Decimal, InvalidOperation
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({
        "status": "Proration API is running",
        "endpoint": "/charge",
        "method": "POST"
    })


@app.post("/charge")
def calculate_charge():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    try:
        old_price = Decimal(str(data["old_price"]))
        new_price = Decimal(str(data["new_price"]))
        days_remaining = Decimal(str(data["days_remaining"]))
        days_in_actual_month = Decimal(str(data["days_in_actual_month"]))
        spec = str(data["spec"]).strip().lower()
    except (KeyError, InvalidOperation, TypeError, ValueError):
        return jsonify({"error": "Invalid or missing request fields"}), 400

    if spec == "v1":
        divisor = Decimal("30")
    elif spec == "v2":
        if days_in_actual_month == 0:
            return jsonify({"error": "days_in_actual_month cannot be zero"}), 400
        divisor = days_in_actual_month
    else:
        return jsonify({"error": "spec must be v1 or v2"}), 400

    charge = (new_price - old_price) * (days_remaining / divisor)

    return jsonify({"charge": float(charge)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
