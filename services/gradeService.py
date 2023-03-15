from src.domain.grade import Grade
from random import randint

from src.undo_redo.undo_redo import Call, Operation


class GradeService:
    def __init__(self, repository, undoredo):
        '''
        Constructor
        :param repository:
        '''
        self.__repo = repository
        self.__undoredo = undoredo

    def generate_random_grades(self):
        '''
        Generates random grades at startup
        :return:
        '''
        for i in range(20):
            grade_id = i + 1
            student_id = randint(1, 10)
            discipline_id = randint(1, 10)
            grade_value = randint(1,10)
            grade = Grade(grade_id, student_id, discipline_id, grade_value)
            self.__repo.store(grade)


    def add_grade(self, grade_id, student_id, discipline_id, grade_value):
        '''
        Creates and adds a student to the student repository
        :param grade_id:
        :param student_id:
        :param discipline_id:
        :param grade_value:
        :return:
        '''
        grade_id = self.__repo.get_length_of_data() + 1
        new_grade = Grade(grade_id, student_id, discipline_id, grade_value)
        self.__repo.store(new_grade)
        undo_call = Call(self.__repo.delete_by_id, new_grade.get_grade_id())
        redo_call = Call(self.__repo.store, new_grade)
        operation = Operation(undo_call, redo_call)
        self.__undoredo.record(operation)

    def remove_grades_student(self, id, operations):
        '''
        Finds and removes all student's grades from the grade repository
        :param id:
        :return:
        '''
        gradesList = self.__repo.get_all_with_id_and_name()
        for grade in gradesList:
            if grade[1] == int(id):
                undo_call = Call(self.__repo.store, Grade(grade[0], grade[1], grade[2], grade[3]))
                redo_call = Call(self.__repo.delete_by_id, grade[0])
                operation = Operation(undo_call, redo_call)
                operations.append(operation)
                self.__repo.delete_by_id(grade[0])

    def remove_disciplines_grades(self, discipline_id, operations):
        '''
        Finds and removes all student's grades at a deleted discipline from the grade repository
        :param discipline_id:
        :return:
        '''
        gradesList = self.__repo.get_all_with_id_and_name()
        for grade in gradesList:
            if grade[2] == int(discipline_id):
                undo_call = Call(self.__repo.store, Grade(grade[0], grade[1], grade[2], grade[3]))
                redo_call = Call(self.__repo.delete_by_id, grade[0])
                operation = Operation(undo_call, redo_call)
                operations.append(operation)
                self.__repo.delete_by_id(grade[0])

    def display_grades(self):
        '''
        Gets all the grades from the grades repository and prints them
        :return:
        '''
        gradesList = self.__repo.get_all_with_id_and_name()
        return gradesList

    def get_repo_data_length(self):
        return self.__repo.get_length_of_data()

    def get_repo_data(self):
        return self.__repo.get_data()