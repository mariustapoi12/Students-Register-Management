import re
import pickle
from src.domain.discipline import Discipline
from src.domain.discipline_validator import DisciplineValidator

class DisciplineRepositoryException(Exception):
    pass

class DisciplineRepository:
    def __init__(self, validator_class):
        self.__validator_class = validator_class
        self._data = {}

    def find_by_id(self, discipline_id):
        if discipline_id in self._data:
            return self._data[discipline_id]
        else:
            return None

    def store(self, discipline):
        self.__validator_class.validate(self, discipline)
        discipline.set_discipline_id(int(discipline.get_discipline_id()))
        if self.find_by_id(discipline.get_discipline_id()) is not None:
            raise DisciplineRepositoryException("Duplicate id {0}.".format(discipline.get_discipline_id()))
        else:
            self._data[discipline.get_discipline_id()] = discipline

    def delete_discipline(self, discipline_id):
        id = int(discipline_id)
        discipline = self.find_by_id(id)
        if discipline == None:
            raise DisciplineRepositoryException("There is no student with this id")
        else:
            self._data.pop(id)

    def update(self, discipline_id, new_name):
        id = int(discipline_id)
        discipline = self.find_by_id(id)
        if discipline == None:
            raise DisciplineRepositoryException("There is no entity with this id")
        else:
            self._data[discipline.get_discipline_id()].set_name(new_name)

    def get_all_with_id_and_name(self):
        list = []
        for discipline in self._data:
            list.append([self._data[discipline].get_discipline_id(), self._data[discipline].get_name()])
        return list

    def get_all_having_likely_id(self, likely_id):
        list = []
        for discipline in self._data:
            entity_id_as_string = str(self._data[discipline].get_discipline_id())
            if re.search(likely_id, entity_id_as_string, re.IGNORECASE):
                list.append([self._data[discipline].get_discipline_id(), self._data[discipline].get_name()])
        return list

    def get_all_having_likely_name(self, likely_name):
        list = []
        for discipline in self._data:
            entity_name_as_string = str(self._data[discipline].get_name())
            if re.search(likely_name, entity_name_as_string, re.IGNORECASE):
                list.append([self._data[discipline].get_discipline_id(), self._data[discipline].get_name()])
        return list

    def get_repo_length(self):
        return len(self._data)

    def get_data(self):
        return self._data

class DisciplineTextFileRepository(DisciplineRepository):
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
        super().__init__(DisciplineValidator)
        #self.__validator_class = validator_class
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rt")  # rt -> read, text-mode
        for line in f.readlines():
            _id, name = line.split(maxsplit=1, sep=',')
            self.store(Discipline(int(_id), name.rstrip()))
        f.close()

    def _save_file(self):
        f = open(self._file_name, "wt")  # wt -> write, text-mode

        for discipl in self._data.values():
            f.write(str(discipl.get_discipline_id()) + ',' + discipl.get_name() + "\n")

        f.close()

    def add(self, entity):
        """
        1. Do whatever the add method in the base class does
        2. Save the ingredients to file
        """
        super(DisciplineTextFileRepository, self).store(entity)
        # super().add(entity)
        self._save_file()

    def update(self, discipline_id, new_name):
        super(DisciplineTextFileRepository, self).update(discipline_id, new_name)
        self._save_file()

    def delete_by_id(self, discipline_id):
        super(DisciplineTextFileRepository, self).delete_discipline(discipline_id)
        self._save_file()

class DisciplineBinFileRepository(DisciplineRepository):
    def __init__(self, file_name):
        super().__init__(DisciplineValidator)
        self._file_name = file_name
        #self._save_file()
        self._load_file()
        self._save_file()

    def _load_file(self):
        file = open(self._file_name, "rb")
        self._disciplinesList = pickle.load(file)
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wb")
        pickle.dump(self._data, file)
        file.close()

    def store(self, discipline):
        super(DisciplineBinFileRepository, self).store(discipline)
        self._save_file()

    def update(self, discipline_id, new_name):
        super(DisciplineBinFileRepository, self).update(discipline_id, new_name)
        self._save_file()

    def delete_by_id(self, discipline_id):
        super(DisciplineBinFileRepository, self).delete_discipline(discipline_id)
        self._save_file()