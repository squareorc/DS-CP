from flask import Flask, render_template, request, jsonify
import networkx as nx
import json

app = Flask(__name__)

# Course dependency graph (hardcoded)
graph = nx.DiGraph()
graph.add_edges_from([
    ("Arrays", "Sorting"),
    ("Sorting", "Binary Search"),
    ("Binary Search", "Graphs"),
    ("Graphs", "Dynamic Programming")
])

# Load user progress from JSON
def load_progress():
    try:
        with open("course_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user progress
def save_progress(progress):
    with open("course_data.json", "w") as file:
        json.dump(progress, file, indent=4)

@app.route("/")
def index():
    # Get sorted course order
    order = list(nx.topological_sort(graph))
    user_progress = load_progress()
    return render_template("dashboard.html", courses=order, progress=user_progress)

@app.route("/mark_complete", methods=["POST"])
def mark_complete():
    data = request.json
    course = data.get("course")

    progress = load_progress()
    progress[course] = True
    save_progress(progress)

    return jsonify({"status": "success", "updated_progress": progress})

if __name__ == "__main__":
    app.run(debug=True)
