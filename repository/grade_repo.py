from src.domain.grade_validator import *
from src.domain.grade import Grade
import pickle

class GradeRepositoryException(Exception):
    pass

class GradeRepository:
    def __init__(self, validator_class):
        self.__validator_class = validator_class
        self._data = {}

    def find_by_id(self, grade_id):
        if grade_id in self._data:
            return self._data[grade_id]
        else:
            return None

    def store(self, grade):
        self.__validator_class.validate(self, grade)
        #grade_id = len(self.__data) + 1
        #grade.set_grade_id(int(grade_id))
        self._data[grade.get_grade_id()] = grade

    def delete_by_id(self, entity_id):
        id = int(entity_id)
        entity = self.find_by_id(id)
        if entity == None:
            raise GradeValidatorException("There is no entity with this id")
        else:
            self._data.pop(id)

    def get_all_with_id_and_name(self):
        list = []
        for grade in self._data:
            list.append([self._data[grade].get_grade_id() ,self._data[grade].get_student_id(),
                         self._data[grade].get_discipline_id(), self._data[grade].get_grade()])
        return list

    def get_length_of_data(self):
        return len(self._data)

    def get_data(self):
        return self._data

class GradeTextFileRepository(GradeRepository):
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
        super().__init__(GradeValidator)
        #self.__validator_class = validator_class
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rt")  # rt -> read, text-mode
        for line in f.readlines():
            _grade_id, student_id, discipline_id, grade_value = line.split(maxsplit=3, sep=',')
            self.store(Grade(int(_grade_id), int(student_id), int(discipline_id), int(grade_value)))
        f.close()

    def _save_file(self):
        f = open(self._file_name, "wt")  # wt -> write, text-mode

        for grd in self._data.values():
            f.write(str(grd.get_grade_id()) + ',' + str(grd.get_student_id()) + ',' + str(grd.get_discipline_id()) +',' +
                    str(grd.get_grade()) +"\n")

        f.close()

    def store(self, entity):
        """
        1. Do whatever the add method in the base class does
        2. Save the ingredients to file
        """
        super(GradeTextFileRepository, self).store(entity)
        # super().add(entity)
        self._save_file()

class GradeBinFileRepository(GradeRepository):
    def __init__(self, file_name):
        super().__init__(GradeValidator)
        self._file_name = file_name
        #self._save_file()
        self._load_file()
        self._save_file()

    def _load_file(self):
        file = open(self._file_name, "rb")
        self._gradesList = pickle.load(file)
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wb")
        pickle.dump(self._data, file)
        file.close()

    def save(self, grade):
        super(GradeBinFileRepository, self).store(grade)
        self._save_file()