from flask import Flask, jsonify, request, render_template, redirect, url_for
from bridge import new_comparison, get_random_objects, compare, get_object_title, show_comparison, show_objects, new_object
import os
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "2023_May_15_19_57"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        comparison_id = new_comparison(title)
        return redirect(url_for('comparison_route', comparison_id=comparison_id))
    comparisons = json.loads(show_comparison())
    return render_template('home.html', comparisons=comparisons)

@app.route('/new', methods=['POST'])
def new_comparison_route():
    title = request.form['title']
    comparison_id = new_comparison(title)
    return redirect(url_for('comparison_route', comparison_id=comparison_id))

@app.route("/<int:comparison_id>/new_object", methods=['POST'])
def new_object_route(comparison_id):
    object_title = request.form['object_title']
    new_object(object_title, comparison_id)
    return redirect(url_for('comparison_route', comparison_id=comparison_id))

@app.route("/<int:comparison_id>", methods=['GET'])
def comparison_route(comparison_id):
    objects = json.loads(show_objects())
    objects = [obj for obj in objects if obj[3] == comparison_id]
    objects.sort(key=lambda x: x[2], reverse=True)
    return render_template('comparison.html', comparison_id=comparison_id, title=get_object_title(comparison_id), objects=objects)

@app.route("/<int:comparison_id>/compare", methods=['GET', 'POST'])
def compare_route(comparison_id):
    if request.method == 'POST':
        winner_id = int(request.form['winner'])
        objects = get_random_objects(comparison_id)
        if objects[0][0] == winner_id:
            compare(objects[0][0], objects[1][0], True)
        else:
            compare(objects[0][0], objects[1][0], False)
        return redirect(url_for('compare_route', comparison_id=comparison_id))
    objects = get_random_objects(comparison_id)
    if not objects or None in objects:
        return jsonify({'error': 'Not enough objects to compare.'}), 400
    return render_template('compare.html', comparison_id=comparison_id, object1=objects[0][1], object2=objects[1][1], object1_id=objects[0][0], object2_id=objects[1][0])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))