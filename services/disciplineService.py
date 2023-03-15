from src.domain.discipline import Discipline
from random import randint

from src.undo_redo.undo_redo import Call, Operation, ComplexOperation


class DisciplineService:
    def __init__(self, repository, undoredo):
        '''
        Constructor
        :param repository:
        '''
        self.__repo = repository
        self.__undoredo = undoredo

    def generate_random_disciplines(self):
        '''
        Generates random disciplines at startup
        :return:
        '''
        names = ["ASC", "LC", "Analysis", "Algebra", "Sport", "C", "C++", "Python2", "Python3", "C#"]
        counter = 1
        n = 10
        for i in range(n):
            id = counter
            random = randint(0, len(names) - 1)
            name = names[random]
            discipline = Discipline(id, name)
            self.__repo.store(discipline)
            names.remove(names[random])
            counter += 1

    def add_discipline(self, discipline_id, name):
        '''
        Creates and adds a student to the student repository
        :param discipline_id:
        :param name:
        :return:
        '''
        new_discipline = Discipline(discipline_id, name)
        self.__repo.store(new_discipline)
        undo_call = Call(self.__repo.delete_discipline, discipline_id)
        redo_call = Call(self.__repo.store, new_discipline)
        operation = Operation(undo_call, redo_call)
        self.__undoredo.record(operation)

    def remove_discipline(self, discipline_id, operations):
        '''
        Removes a student from the student repository
        :param discipline_id:
        :return:
        '''
        old_discipline = self.__repo.find_by_id(discipline_id)
        undo_call = Call(self.__repo.store, old_discipline)
        redo_call = Call(self.__repo.delete_discipline, discipline_id)
        self.__repo.delete_discipline(discipline_id)
        operations.append(Operation(undo_call, redo_call))
        self.__undoredo.record(ComplexOperation(operations))

    def update_discipline(self, discipline_id, new_name):
        '''
        Changes the student's name with the new one
        :param discipline_id:
        :param new_name:
        :return:
        '''
        old_name = self.__repo.find_by_id(discipline_id).get_name()
        self.__repo.update(discipline_id, new_name)
        undo_call = Call(self.__repo.update, discipline_id, old_name)
        redo_call = Call(self.__repo.update, discipline_id, new_name)
        operation = Operation(undo_call, redo_call)
        self.__undoredo.record(operation)

    def display_disciplines(self):
        '''
        Gets all the students from the student repository and prints them
        :return:
        '''
        disciplinesList = self.__repo.get_all_with_id_and_name()
        return disciplinesList

    def search_disciplines_by_id(self, discipline_id):
        disciplinesList = self.__repo.get_all_having_likely_id(discipline_id)
        return disciplinesList

    def search_disciplines_by_name(self, discipline_name):
        disciplinesList = self.__repo.get_all_having_likely_name(discipline_name)
        return disciplinesList

    def get_repo_data_length(self):
        return self.__repo.get_repo_length()

    def get_repo_data(self):
        return self.__repo.get_data()