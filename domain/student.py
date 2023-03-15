class Student():
    def __init__(self, student_id, name):
        '''
        Initialize the student object
        :param student_id:
        :param name:
        '''
        self._student_id = student_id
        self._name = name

    def get_student_id(self):
        return self._student_id

    def get_name(self):
        return  self._name

    def set_name(self, name):
        self._name = name

    def set_student_id(self, id):
        self._student_id = id

    """def __str__(self):
        return "Id:" + str(self.id) + " Name:" + str(self.name)"""