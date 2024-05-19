import json

def load(filename):
    """Loads a JSON file as a database."""
    try:
        with open(filename, "r") as test_file:
            test_data = json.load(test_file)
        return sort_database(test_data, "project_id", rev=True)
    except Exception as err:
        print("there was an error loading the database: ", err)
        return []


def get_project_count(database):
    """Returns the number of projects in the loaded database."""
    return len(database)


def get_project(db, project_id):
    """Retrieves a project with the given ID from the loaded database."""
    return next((project for project in db if project["project_id"] == project_id), None)


def get_techniques(database):
    """Returns all techniques existing in the 'techniques_used' fields in the database."""
    return sorted({tec for dictionary in database for tec in dictionary["techniques_used"]})


def get_technique_stats(database):
    """Creates a dictionary with the technique as key, adds all projects as a dict with name and ID."""
    technique_list = get_techniques(database)
    return {
        technique: [
            {"id": project["project_id"], "name": project["project_name"]}
            for project in database if technique in project["techniques_used"]
        ]
        for technique in technique_list
    }


def search(db, sort_by="start_date", sort_order="desc", techniques=None, search=None, search_fields=None):
    """Search function that returns projects matching the input search criteria."""
    db = sort_database(db, sort_by, sort_order != "desc")

    if search_fields is None:
        search_fields = [key for project in db for key in project]

    if techniques:
        db = [project for project in db if all(tech in project["techniques_used"] for tech in techniques)]

    if search:
        search = search.lower()
        db = [project for project in db if any(search in str(project.get(field, "")).lower() for field in search_fields)]

    return db

                 
##################################################

# Sortering åt båda håll fungerar. Man kan skickar med ett valfritt argument.
def sort_database(database, key_to_sort_by=None, rev=False):
    """Sorts database on a keyword, reverse the list using rev=True."""
    if not database:  # if database empty eller None
        return []

    try:
        if key_to_sort_by and all(key_to_sort_by in dictionary for dictionary in database):
            return sorted(database, reverse=rev, key=lambda x: x.get(key_to_sort_by))
        else:
            return database
    except Exception as err:
        print("There was an error sorting the database: ", err)
        return []


def get_search_fields():
    """Help function to send along the search field names to the Flask preprocessor."""
    search_fields = [
        "project_name",
        "start_date",
        "end_date",
        "group_size",
        "short_description",
        "long_description",
        "academic_credits",
        "course_name"]
    return list(search_fields)


def get_projects_from_id(db, search_variable):
    """Retrieves projects associated with a given technique ID."""
    tech_stats = get_technique_stats(db)
    if search_variable in tech_stats:
        return [get_project(db, proj["id"]) for proj in tech_stats[search_variable]]
    return []


##################################################


if __name__ == "__main__":
    db = load("data.json")
    # print(db)
    # techs = ["python"]
    # print(get_project(db, 2))
    # print(get_techinques(db))
    # print(sort_database(db, "course_name"))
    # print(get_technique_stats(db))
    # print(tech_stats["python"][0])
    # print(len(tech_stats))
    # print(search(db, sort_by="group_size"))
    # print(search(db, search="no", techniques=["python"], search_fields=["long_description"]))
    # print(get_technique_stats(db))
    # print(get_search_fields())
    get_projects_from_id(db, search_variable="python")
