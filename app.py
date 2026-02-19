from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory inventory storage
inventory = []

# Agent Logic
def get_status(quantity, minimum):
    if quantity < minimum:
        return "Low Stock"
    return "Healthy"

def get_stock_percentage(quantity, minimum):
    if minimum == 0:
        return 100
    return int((quantity / minimum) * 100)

@app.route("/")
def dashboard():
    return render_template("dashboard.html", inventory=inventory)

@app.route("/add", methods=["POST"])
def add_item():
    item = request.form["item"]
    quantity = int(request.form["quantity"])
    minimum = int(request.form["minimum"])

    inventory.append({
        "item": item,
        "quantity": quantity,
        "minimum": minimum,
        "status": get_status(quantity, minimum),
        "percentage": get_stock_percentage(quantity, minimum)
    })

    return redirect(url_for("dashboard"))

@app.route("/delete/<int:index>")
def delete_item(index):
    if index < len(inventory):
        inventory.pop(index)
    return redirect(url_for("dashboard"))

@app.route("/restock")
def restock():
    recommendations = []

    for item in inventory:
        if item["quantity"] < item["minimum"]:
            suggested = item["minimum"] * 2
            recommendations.append({
                "item": item["item"],
                "current": item["quantity"],
                "minimum": item["minimum"],
                "suggested": suggested
            })

    return render_template("restock.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
