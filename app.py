from flask import Flask, render_template, request
from collections import deque

app = Flask(__name__)

class CoursePlanner:
    def __init__(self):
        self.graph = {}
        self.in_degree = {}

    def add_course(self, course, prerequisites):
        if course not in self.graph:
            self.graph[course] = []
            self.in_degree[course] = 0
        
        for pre in prerequisites:
            if pre not in self.graph:
                self.graph[pre] = []
                self.in_degree[pre] = 0
            
            self.graph[pre].append(course)
            self.in_degree[course] += 1

    def find_learning_order(self):
        queue = deque([course for course in self.graph if self.in_degree[course] == 0])
        order = []

        while queue:
            course = queue.popleft()
            order.append(course)

            for neighbor in self.graph[course]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return order if len(order) == len(self.graph) else ["Cycle detected, check prerequisites"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topics = request.form.getlist("topic[]")
        prerequisites = request.form.getlist("prerequisite[]")

        planner = CoursePlanner()
        for topic, pre in zip(topics, prerequisites):
            planner.add_course(topic, pre.split(","))  

        order = planner.find_learning_order()
        return render_template("result.html", order=order)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
