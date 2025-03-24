from flask import Flask, render_template, request, jsonify
import networkx as nx
import json

app = Flask(__name__)

# Load course data (Graph structure)
def load_courses():
    try:
        with open("course_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "courses": {
                "Arrays": [],
                "Sorting": ["Arrays"],
                "Binary Search": ["Sorting"],
                "Graphs": ["Binary Search"],
                "Dynamic Programming": ["Graphs"]
            },
            "progress": {}
        }

def save_courses(data):
    with open("course_data.json", "w") as file:
        json.dump(data, file, indent=4)

# Initialize graph
def build_graph(course_data):
    graph = nx.DiGraph()
    for course, prereqs in course_data["courses"].items():
        for prereq in prereqs:
            graph.add_edge(prereq, course)
    return graph

@app.route("/")
def index():
    course_data = load_courses()
    graph = build_graph(course_data)
    sorted_courses = list(nx.topological_sort(graph))
    return render_template("index.html", courses=course_data["courses"], progress=course_data["progress"], sorted_courses=sorted_courses)

@app.route("/mark_complete", methods=["POST"])
def mark_complete():
    data = request.json
    course = data.get("course")
    
    course_data = load_courses()
    prerequisites = course_data["courses"].get(course, [])
    
    # Check if prerequisites are done
    if not all(course_data["progress"].get(prereq, False) for prereq in prerequisites):
        return jsonify({"status": "error", "message": "Complete prerequisites first!"})
    
    # Mark as completed
    course_data["progress"][course] = True
    save_courses(course_data)
    
    # Get next recommended courses
    next_courses = [c for c in course_data["courses"] if c not in course_data["progress"]]
    
    return jsonify({"status": "success", "updated_progress": course_data["progress"], "next_courses": next_courses})

@app.route("/add_course", methods=["POST"])
def add_course():
    data = request.json
    course_name = data.get("course")
    prerequisites = data.get("prerequisites", [])

    course_data = load_courses()
    course_data["courses"][course_name] = prerequisites
    save_courses(course_data)

    return jsonify({"status": "success", "courses": course_data["courses"]})

if __name__ == "__main__":
    app.run(debug=True)
