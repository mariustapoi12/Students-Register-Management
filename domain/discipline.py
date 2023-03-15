class Discipline:
    def __init__(self, discipline_id, name):
        '''
        Initialize the discipline object
        :param discipline_id:
        :param name:
        '''
        self._discipline_id = discipline_id
        self._name = name

    def get_discipline_id(self):
        return self._discipline_id

    def get_name(self):
        return  self._name

    def set_name(self, name):
        self._name = name

    def set_discipline_id(self, id):
        self._discipline_id = id