"""

week0 project for 'cs50 introduction to artificial intelligence'
https://cs50.harvard.edu/ai/2020/projects/0/degrees/

"""

import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")

        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source: str, target: str):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # Start with a frontier that contains the initial state
    source_node: Node = Node(state=source, parent=None, action=neighbors_for_person(source))
    frontier: QueueFrontier = QueueFrontier()  # Breadth-first search to guarantee shortest-path is found
    frontier.add(source_node)

    # Start with an empty explored set
    explored_nodes: set = set()
    num_nodes_explored = 0

    # If node contains goal state, return the solution
    if source_node == target:
        return get_path_to_source(source_node)

    while True:

        # If the frontier is empty, then no solution
        if frontier.empty():
            raise Exception(f"No path found from {source} to {target}")

        # Remove node from the frontier
        current_node: Node = frontier.remove()

        # # Reporting (comment in to see progress reporting)
        # num_nodes_explored += 1
        # print(f"Exploring node {num_nodes_explored}: {person_name_for_id(current_node.state)}")

        # Add the node to the explored set
        explored_nodes.add(current_node.state)

        # Expand node, add resulting nodes to the frontier if they aren't already in the frontier or the explored set
        for action, state in neighbors_for_person(current_node.state):
            if not (frontier.contains_state(state)) and (state not in explored_nodes):
                child_node = Node(state=state, parent=current_node, action=action)

                # Check child node == target node before adding to frontier
                # If child node == target node, then get path back to source
                if child_node.state == target:
                    return get_path_to_source(child_node)

                frontier.add(child_node)


def get_path_to_source(node):
    path = []

    while node.parent is not None:
        path.append((node.action, node.state))
        node = node.parent
    path.reverse()
    return path


def person_name_for_id(person_id):
    return people.get(person_id)['name']


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
