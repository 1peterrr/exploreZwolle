from flask import Flask, render_template, request, redirect, url_for
from database import (
    create_tables,
    get_recommendations,
    add_recommendation,
    get_recommendation_by_id,
    update_recommendation, 
    delete_recommendation
)

app = Flask(__name__)

create_tables()

@app.route("/")
def home():
    search = request.args.get("search", "")
    category = request.args.get("category", "")

    recommendations = get_recommendations(
        search,
        category
    )

    return render_template(
        "index.html",
        recommendations=recommendations,
        search=search,
        category=category
    )

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        category = request.form["category"]

        if category == "Other":
            category = request.form["other_category"]
        
        rating = request.form["rating"]
        description = request.form["description"]
        image_url = request.form["image_url"]
        recommended_by = request.form["recommended_by"]

        add_recommendation(
            name,
            location,
            category,
            rating,
            description,
            image_url,
            recommended_by
        )

        return redirect(url_for("home"))

    return render_template("add.html")


@app.route("/edit/<int:recommendation_id>", methods=["GET", "POST"])
def edit(recommendation_id):
    recommendation = get_recommendation_by_id(recommendation_id)

    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        category = request.form["category"]

        if category == "Other":
            category = request.form["other_category"]

        rating = request.form["rating"]
        description = request.form["description"]
        image_url = request.form["image_url"]
        recommended_by = request.form["recommended_by"]

        update_recommendation(
            recommendation_id,
            name,
            location,
            category,
            rating,
            description,
            image_url,
            recommended_by
        )

        return redirect(url_for("home"))

    return render_template(
        "edit.html",
        recommendation=recommendation
    )

@app.route("/delete/<int:recommendation_id>", methods=["POST"])
def delete(recommendation_id):
    delete_recommendation(recommendation_id)

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)