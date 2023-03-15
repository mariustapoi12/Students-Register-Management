from src.domain.student import Student
from random import randint

from src.undo_redo.undo_redo import Call, Operation, ComplexOperation


class StudentService():
    def __init__(self, repoistory, undoredo):
        '''
        Constructor
        :param repoistory:
        '''
        self.__repo = repoistory
        self.__undoredo = undoredo

    def generate_random_students(self):
        '''
        Generates random students at startup
        :return:
        '''
        names = ["Tapoi", "Rus", "Turcu", "Musk", "Pop", "Ardelean", "Anghel", "Malai", "Joaca-Bine", "Tapoioi", "Tapoy",
                 "Baciu", "Tapy", "Cont"]
        counter = 1
        n = 10
        for i in range(n):
            id = counter
            random = randint(0, len(names) - 1)
            name = names[random]
            student = Student(id, name)
            self.__repo.store(student)
            names.remove(names[random])
            counter += 1

    def add_student(self, student_id, name):
        '''
        Creates and adds a student to the student repository
        :param student_id:
        :param name:
        :return:
        '''
        new_student = Student(student_id, name)
        self.__repo.store(new_student)
        undo_call = Call(self.__repo.delete_student, student_id)
        redo_call = Call(self.__repo.store, new_student)
        operation = Operation(undo_call, redo_call)
        self.__undoredo.record(operation)

    def remove_student(self, student_id, operations):
        '''
        Removes a student from the student repository
        :param student_id:
        :return:
        '''
        old_student = self.__repo.find_by_id(student_id)
        undo_call = Call(self.__repo.store, old_student)
        redo_call = Call(self.__repo.delete_student, student_id)
        self.__repo.delete_student(student_id)
        operations.append(Operation(undo_call, redo_call))
        self.__undoredo.record(ComplexOperation(operations))


    def update_student(self, student_id, new_name):
        '''
        Changes the student's name with the new one
        :param student_id:
        :param new_name:
        :return:
        '''
        old_name = self.__repo.find_by_id(student_id).get_name()
        self.__repo.update(student_id, new_name)
        undo_call = Call(self.__repo.update, student_id, old_name)
        redo_call = Call(self.__repo.update, student_id, new_name)
        operation = Operation(undo_call, redo_call)
        self.__undoredo.record(operation)

    def display_students(self):
        '''
        Gets all the students from the student repository and prints them
        :return:
        '''
        studentsList = self.__repo.get_all_with_id_and_name()
        return studentsList

    def search_students_by_id(self, student_id):
        studentsList = self.__repo.get_all_having_likely_id(student_id)
        return studentsList

    def search_students_by_name(self, student_name):
        studentsList = self.__repo.get_all_having_likely_name(student_name)
        return studentsList

    def get_repo_data_length(self):
        return self.__repo.get_repo_length()

    def get_repo_data(self):
        return self.__repo.get_data()