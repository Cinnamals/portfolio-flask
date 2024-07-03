#!/usr/bin/env python3
from flask import Flask, render_template, request
from data import *

app = Flask("portfolio")
data = load("data.json")


@app.context_processor
def global_variables():
    data = load("data.json")
    return {
        'list_of_techniques': get_techniques(data),
        'list_of_fields': get_search_fields()
    }


@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/techniques")
def techniques():
    tech_list = get_techniques(data)
    return render_template("techniques.html", list_of_techniques=tech_list)


@app.route("/projects/<search_val>")
def projects(search_val):
    title = str("")
    data = load("data.json")
    project_list = []

    if search_val == 'all':
        project_list = search(data)
        title = "All projects"
    else:
        project_list = get_projects_from_id(data, search_val)
        title = search_val.title()
        if project_list == []:
            return render_template("404.html")

    return render_template("projects.html", list_of_projects=project_list, title=title)


@app.route("/project/<project_id>")
def project(project_id):
    project = {}
    title = ""
    data = load("data.json")

    if data == None:
        title = "Page not found!"
        return render_template("404.html")
    for d in data:
        if int(d["project_id"]) == int(project_id):
            title = d["project_name"]
            project = d

    return render_template("project.html", project_to_render=project, title=title)


@app.route("/search/", methods=['GET', 'POST'])
def search_site():
    if request.method == 'POST':
        searchargs = request.form.to_dict(flat=False)

        search_term = searchargs.get("searchterm", [""])
        tech_arg = searchargs.get("tech")
        sort_by_arg = searchargs.get("sortby", ["start_date"])
        sort_order_arg = searchargs.get("sortorder", ["desc"])
        allowed_field_arg = searchargs.get("f")
        title = "Projects"

        try:
            data = load("data.json")
            result = search(data, search=search_term[0], techniques=tech_arg,
                            sort_order=sort_order_arg[0], sort_by=sort_by_arg[0], search_fields=allowed_field_arg)
        except Exception as err:
            print("there was an error with the search result: ", err)
            result = []

        return render_template("projects.html", list_of_projects=result, title=title)
    else:
        return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)
