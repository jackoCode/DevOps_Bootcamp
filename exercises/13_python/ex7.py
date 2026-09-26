class Person:
    """Person class."""
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def full_name(self):
        print(self.first_name, self.last_name)


class Student(Person):
    """Student class."""
    def __init__(self, first_name, last_name, age):
        super().__init__(first_name, last_name, age)
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.lectures_attend = []

    def list_lectures(self):
        if len(self.lectures_attend) == 0:
            print('Dose not attend any lectures.')

        for lecture in self.lectures_attend:
            print(lecture)

    def add_lecture(self, new_lecture):
        self.lectures_attend.append(new_lecture)

    def remove_lecture(self, lecture_to_remove):
        self.lectures_attend.remove(lecture_to_remove)


class Professor(Student):
    """Professor class."""
    def __init__(self, first_name, last_name, age):
        super().__init__(first_name, last_name, age)
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.subjects = []

    def list_subjects(self):
        if len(self.subjects) == 0:
            print('Dose not attend any lectures.')

        for lecture in self.subjects:
            print(lecture)

    def add_subject(self, new_subject):
        self.subjects.append(new_subject)

    def remove_subject(self, subject_to_remove):
        self.subjects.remove(subject_to_remove)


class Lecture:
    """Lecture class."""
    def __init__(self, name, max_no_of_students, duration):
        self.name = name
        self.max_no_of_students = max_no_of_students
        self.duration = duration
        self.lecture_profs = []

    def print_name_duration(self):
        print(self.name, self.duration)

    def add_prof(self, prof):
        self.lecture_profs.append(prof)


def main():
    student = Student(
        first_name='John',
        last_name='Smith',
        age=30,
    )

    student.full_name()
    student.add_lecture('Math')
    student.add_lecture('Computer Science')
    student.list_lectures()
    student.remove_lecture('Math')
    student.list_lectures()


if __name__ == '__main__':
    main()
