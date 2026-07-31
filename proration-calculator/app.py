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
    try:
        data = request.get_json(force=True)

        old_price = float(data["old_price"])
        new_price = float(data["new_price"])
        days_remaining = float(data["days_remaining"])
        days_in_actual_month = float(data["days_in_actual_month"])
        spec = data["spec"]

        price_difference = new_price - old_price

        if spec == "v1":
            divisor = 30
        elif spec == "v2":
            if days_in_actual_month <= 0:
                return jsonify({
                    "error": "days_in_actual_month must be greater than 0"
                }), 400
            divisor = days_in_actual_month
        else:
            return jsonify({
                "error": "spec must be either v1 or v2"
            }), 400

        charge = price_difference * (days_remaining / divisor)

        return jsonify({
            "charge": charge
        })

    except (KeyError, TypeError, ValueError) as error:
        return jsonify({
            "error": f"Invalid request: {str(error)}"
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
