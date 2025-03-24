$(document).ready(function() {
    loadGraph();
});

function markCompleted(course) {
    fetch('/mark_complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "course": course })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            document.getElementById(course).classList.add("completed");
            updateRecommendations(data.next_courses);
        } else {
            alert(data.message);
        }
    });
}

function updateRecommendations(nextCourses) {
    let list = document.getElementById("recommended-courses");
    list.innerHTML = "";
    nextCourses.forEach(course => {
        let item = document.createElement("li");
        item.textContent = course;
        list.appendChild(item);
    });
}

function addCourse() {
    let course = document.getElementById("new-course").value;
    let prereqs = document.getElementById("prereqs").value.split(",").map(c => c.trim());

    fetch('/add_course', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "course": course, "prerequisites": prereqs })
    })
    .then(response => response.json())
    .then(data => {
        location.reload();
    });
}

function loadGraph() {
    fetch('/static/course_data.json')
    .then(response => response.json())
    .then(data => {
        let nodes = Object.keys(data.courses).map(course => ({ id: course, label: course }));
        let edges = [];
        for (let course in data.courses) {
            data.courses[course].forEach(prereq => {
                edges.push({ from: prereq, to: course });
            });
        }

        let container = document.getElementById("network-graph");
        let graphData = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
        let options = { edges: { arrows: "to" } };
        new vis.Network(container, graphData, options);
    });
}
