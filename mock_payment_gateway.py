from flask import Flask, jsonify, request

##from Samples.service_a.app import process_payment

app = Flask(__name__)

@app.route("/api/pay", methods=["POST"])
def pay():
    return jsonify({"status": "payment processed"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
    print("Status",process_payment())
