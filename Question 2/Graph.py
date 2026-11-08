class DirectedGraph:
    #Construct the unweighted undirected graph object
    def __init__(self):
        self.outgoing = {}
        self.incoming = {}

    def add_vertex(self, vertex):
        #Add vertex to the graph if it does not already exist
        if vertex not in self.outgoing:
            self.outgoing[vertex] = {}
            self.incoming[vertex] = {}

    def remove_vertex(self, vertex):
       #Remove a vertex and every edge connected to it.
        if vertex not in self.outgoing:
            return False
        for y in list(self.outgoing[vertex]):  #Delete incoming edges
            del self.incoming[y][vertex]

        for x in list(self.incoming[vertex]):  #Delete outgoing edges
            del self.outgoing[x][vertex]

        del self.outgoing[vertex]
        del self.incoming[vertex]
        return True

    def add_edge(self, x, y):
        #Connect vertex u to vertex v
        self.add_vertex(x)
        self.add_vertex(y)
        self.outgoing[x][y] = None #y is unlocked by x
        self.incoming[y][x] = None #x is a prerequisite of y

    def remove_edge(self, x, y):
        removed = False
        if x in self.outgoing and y in self.outgoing[x]:
            del self.outgoing[x][y]
            removed = True
        if y in self.incoming and x in self.incoming[y]:
            del self.incoming[y][x]
            removed = True
        return removed


    def get_incoming_vertex(self, vertex):
        return self.incoming.get(vertex, {})

    def get_outgoing_vertex(self, vertex):
        return self.outgoing.get(vertex, {})

    def get_all_vertices(self):
        return list(self.outgoing.keys())


class Course:
    # Construct the course object
    def __init__(self, course_code, course_name, credit_hours, level):
        self.course_code = course_code.upper()
        self.course_name = course_name
        self.credit_hours = int(credit_hours)
        self.level = level.capitalize()  #"Core" or "Elective"

    #Make Course object hashable so it can be used as a graph vertex
    def __hash__(self):
        return hash(self.course_code)

    def __eq__(self, other):
        if isinstance(other, Course):
            return self.course_code == other.course_code
        return False

    def __str__(self):
        return f"{ self.course_code:<5} - {self.course_name}"

    def display_details(self):

        print("\n" + "=" * 40)
        if self.level == "Elective":
            print(f"Course Name: {self.course_name}")
            print("Level: Elective (Details hidden)")
        else:
            print(f"Course Code  : {self.course_code}")
            print(f"Course Name  : {self.course_name}")
            print(f"Credit Hours : {self.credit_hours}")
            print(f"Level        : {self.level}")
        print("=" * 40)


def seed_data():
    #Initializes the graph and sample courses with prerequisite relationships.
    graph = DirectedGraph()

    #Sample Courses
    courses = {
        "4000CMD": Course("4000CMD", "Programming: Concepts and Algorithms", 5, "Core"),
        "4002CMD": Course("4002CMD", "Computer Systems", 5, "Core"),
        "4001CMD": Course("4001CMD", "Mathematical Skills for Computing Professionals", 5, "Core"),
        "4003CMD": Course("4003CMD", "Programming: Professional Practice", 5, "Core"),
        "4005CMD": Course("4005CMD", "Integrative Project", 5, "Core"),
        "5022CMD": Course("5022CMD", "Advanced Algorithms", 5, "Elective"),
        "5024CMD": Course("5024CMD", "Data Science", 5, "Elective"),
        "5027CMD": Course("5027CMD", "Web Development", 5, "Elective"),
    }

    # Add all courses as vertices in the graph
    for course in courses.values():
        graph.add_vertex(course)

    # Set up Prerequisite Edges
    # 4000CMD is a prerequisite for 4003CMD
    graph.add_edge(courses["4000CMD"], courses["4003CMD"])
    graph.add_edge(courses["4000CMD"], courses["4005CMD"])
    graph.add_edge(courses["4000CMD"], courses["5027CMD"])

    # 4001CMD is a prerequisite for 5022CMD
    graph.add_edge(courses["4001CMD"], courses["5022CMD"])

    return graph, courses


def find_course(courses):
    #Helper function to find a course object by its course code input.
    code = input("Enter Course Code (e.g., 4000CMD): ").strip().upper()
    if code in courses:
        return courses[code]
    print(f"Course with code '{code}' not found.")
    return None

def menu():
    print("\n=== University Course Prerequisite System ===")
    print("1. List all courses")
    print("2. View course details")
    print("3. List prerequisites for a course")
    print("4. List courses unlocked by a course")
    print("5. Add a new course")
    print("6. Delete a course")
    print("7. Add a prerequisite course")
    print("8. Remove a prerequisite course")
    print("9. Exit")


def main():
    graph, courses = seed_data()

    while True:

        menu()

        choice = input("Enter your choice (1-9): ")

        match choice:

            case '1':
                print("\n=== List of All Courses ===")

                i = 1
                for course in courses.values():
                    print(f"{i}. {course}")
                    i += 1

            case '2':
                course = find_course(courses)
                if course:
                    course.display_details()

            case '3':
                course = find_course(courses)
                if course:
                    prerequisites = graph.get_incoming_vertex(course)
                    print(f"\nPrerequisites for {course.course_code}:")
                    if prerequisites:
                        for p in prerequisites:
                            print(f" - {p}")
                    else:
                        print(" - None (No prerequisites required)")

            case '4':
                course = find_course(courses)
                if course:
                    unlocked = graph.get_outgoing_vertex(course)
                    print(f"\nCourses unlocked by {course.course_code}:")
                    if unlocked:
                        for u in unlocked:
                            print(f" - {u}")
                    else:
                        print(" - None")

            case '5':
                print("\n=== Add A New Course ===")
                code = input("Enter Course Code: ").strip().upper()
                if code in courses:
                    print("Course code already exists.")
                    continue
                name = input("Enter Course Name: ").strip().capitalize()

                try:
                    credits = int(input("Enter Credit Hours: ").strip())
                except ValueError:
                    print("Invalid credit hours. Must be a number.")
                    continue
                level = input("Enter Level (Core / Elective): ").strip().capitalize()
                if level not in ['Core', 'Elective']:
                    print("Invalid level. Please enter Core / Elective only.")
                    continue

                new_course = Course(code, name, credits, level)
                courses[code] = new_course
                graph.add_vertex(new_course)
                print(f"Course {code} added successfully!")

            case '6':
                print("\n--- Delete a Course ---")
                course = find_course(courses)
                if course:

                    confirm = input(
                        f"Delete {course.course_code} - {course.course_name}? "
                        f"This also removes it from any prerequisite relationships. (y/n): "
                    ).strip().lower()

                    if confirm == 'y':
                        graph.remove_vertex(course)
                        del courses[course.course_code]
                        print(f"Course {course.course_code} deleted.")
                    else:
                        print("Deletion cancelled.")

            case '7':
                print("\n=== Add Prerequisite Relationship ===")
                print("Specify Course X and its Prerequisite Y (Y is required before X)")
                print("Select Course X:")
                course_x = find_course(courses)

                if course_x:
                    print("Select Course Y:")
                    course_y = find_course(courses)
                    if course_y:
                        if course_x == course_y:
                            print("A course cannot be a prerequisite of itself.")
                        else:
                            graph.add_edge(course_y, course_x)
                            print(f"{course_y.course_code} is now a prerequisite for {course_x.course_code}.")

            case '8':
                print("\n--- Remove Prerequisite Relationship ---")
                print("Select Course X:")
                course_x = find_course(courses)

                if course_x:
                    print("Select Prerequisite Y to remove:")
                    course_y = find_course(courses)
                    if course_y:
                        if graph.remove_edge(course_y, course_x):
                            print(f"Prerequisite {course_y.course_code} removed from {course_x.course_code}.")
                        else:
                            print(f"Course {course_y.course_code} is not a prerequisite of {course_x.course_code}.")

            case '9':
                print("\nExiting program...")
                break

            case _:
                print("Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()