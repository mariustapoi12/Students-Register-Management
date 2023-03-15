from src.domain.student_validator import *
from src.domain.student import Student
import re
import pickle

class StudRepository:
    def __init__(self, validator_class):
        self.__validator_class = validator_class
        self._data = {}

    def find_by_id(self, student_id):
        if student_id in self._data:
            return self._data[student_id]
        else:
            return None

    def store(self, student):
        # raise RepositoryException("duplicate id {0}.".format(entity.get_id()))
        self.__validator_class.validate(self, student)
        student.set_student_id(int(student.get_student_id()))
        if self.find_by_id(student.get_student_id()) is not None:
            raise StudentValidatorException("Invalid id")
        else:
            self._data[student.get_student_id()] = student

    def delete_student(self, student_id):
        id = int(student_id)
        student = self.find_by_id(id)
        if student == None:
            raise StudentValidatorException("There is no student with this id")
        else:
            self._data.pop(id)

    def update(self, student_id, new_name):
        id = int(student_id)
        student = self.find_by_id(id)
        if student == None:
            raise StudentValidatorException("There is no entity with this id")
        else:
            self._data[student.get_student_id()].set_name(new_name)

    def get_all_with_id_and_name(self):
        list = []
        for student in self._data:
            list.append([self._data[student].get_student_id(), self._data[student].get_name()])
        return list

    def get_all_having_likely_id(self, likely_id):
        list = []
        for student in self._data:
            entity_id_as_string = str(self._data[student].get_student_id())
            if re.search(likely_id, entity_id_as_string, re.IGNORECASE):
                list.append([self._data[student].get_student_id(), self._data[student].get_name()])
        return list

    def get_all_having_likely_name(self, likely_name):
        list = []
        for student in self._data:
            entity_name_as_string = str(self._data[student].get_name())
            if re.search(likely_name, entity_name_as_string, re.IGNORECASE):
                list.append([self._data[student].get_student_id(), self._data[student].get_name()])
        return list

    def get_repo_length(self):
        return len(self._data)

    def get_data(self):
        return self._data

class StudentTextFileRepository(StudRepository):
    """
    class TextFileRepository inherits from Repository
        Repository -> base class
        TextFileRepository -> derived class, child class
    what are the effects of this inheritance?
        TextFileRepository has all the non-private methods and fields of Repository
        TextFileRepository has the behaviour of its base class
    what does this mean?
        derived class can do everything that the base class can
        derived class might add some new functionality, or work in a different way
    """

    def __init__(self, file_name):
        super().__init__(StudentValidator)
        #self.__validator_class = validator_class
        self._file_name = file_name
        self._load_file()
        self._save_file()

    def _load_file(self):
        f = open(self._file_name, "rt")  # rt -> read, text-mode
        for line in f.readlines():
            _id, name = line.split(maxsplit=1, sep=',')
            self.store(Student(int(_id), name.rstrip()))
        f.close()

    def _save_file(self):
        f = open(self._file_name, "wt")  # wt -> write, text-mode

        for stud in self._data.values():
            f.write(str(stud.get_student_id()) + ',' + stud.get_name() + "\n")

        f.close()

    def store(self, entity):
        """
        1. Do whatever the add method in the base class does
        2. Save the ingredients to file
        """
        super(StudentTextFileRepository, self).store(entity)
        # super().add(entity)
        self._save_file()

    def update(self, student_id, new_name):
        super(StudentTextFileRepository, self).update(student_id, new_name)
        self._save_file()

    def delete_by_id(self, student_id):
        super(StudentTextFileRepository, self).delete_student(student_id)
        self._save_file()

class StudentBinFileRepository(StudRepository):
    def __init__(self, file_name):
        super().__init__(StudentValidator)
        self._file_name = file_name
        #self._save_file()
        self._load_file()
        self._save_file()

    def _load_file(self):
        file = open(self._file_name, "rb")
        self._studentsList = pickle.load(file)
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wb")
        pickle.dump(self._data, file)
        file.close()

    def store(self, student):
        super(StudentBinFileRepository, self).store(student)
        self._save_file()

    def update(self, student_id, new_name):
        super(StudentBinFileRepository, self).update(student_id, new_name)
        self._save_file()

    def delete_by_id(self, student_id):
        super(StudentBinFileRepository, self).delete_student(student_id)
        self._save_file()
