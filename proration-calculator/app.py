from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Proration API is running",
        "endpoint": "/charge",
        "method": "POST"
    })


@app.route("/charge", methods=["POST"])
def calculate_charge():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        old_price = float(data["old_price"])
        new_price = float(data["new_price"])
        days_remaining = float(data["days_remaining"])
        spec = str(data["spec"]).strip().lower()
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid or missing fields"}), 400

    price_difference = new_price - old_price

    if spec == "v1":
        # v1 must always use exactly 30.
        charge = price_difference * (days_remaining / 30.0)

    elif spec == "v2":
        try:
            days_in_actual_month = float(data["days_in_actual_month"])
        except (KeyError, TypeError, ValueError):
            return jsonify({
                "error": "Invalid days_in_actual_month"
            }), 400

        if days_in_actual_month <= 0:
            return jsonify({
                "error": "days_in_actual_month must be greater than zero"
            }), 400

        charge = price_difference * (
            days_remaining / days_in_actual_month
        )

    else:
        return jsonify({
            "error": "spec must be v1 or v2"
        }), 400

    return jsonify({
        "charge": charge
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
