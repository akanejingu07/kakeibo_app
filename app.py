from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data.json"

# ----------------------
# JSONファイル読み書き
# ----------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ----------------------
# ルーティング
# ----------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date = request.form.get("date")
        type_ = request.form.get("type")  # income / expense
        category = request.form.get("category")
        amount = request.form.get("amount")
        memo = request.form.get("memo")

        new_record = {
            "id": int(datetime.now().timestamp()), 
            "date": date,
            "type": type_,
            "category": category,
            "amount": int(amount),
            "memo": memo,
            "created_at": datetime.now().isoformat()
        }

        data = load_data()
        data.append(new_record)
        save_data(data)

        return redirect(url_for("index"))

    data = load_data()
    data = sorted(data, key=lambda x: x["date"], reverse=True)
    return render_template("index.html", records=data)

# 削除
@app.route("/delete", methods=["POST"])
def delete():
    record_id = request.form.get("record_id")
    print("削除ID:", record_id)

    data = load_data()
    print("削除前:", data)

    data = [r for r in data if str(r.get("id")) != record_id]

    print("削除後:", data)
    save_data(data)

    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run()
