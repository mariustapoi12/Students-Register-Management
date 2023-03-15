class Grade:
    def __init__(self, grade_id, student_id, discipline_id, grade_value):
        self.__grade_id = grade_id
        self.__student_id = student_id
        self.__discipline_id = discipline_id
        self.__grade_value = grade_value

    def get_grade_id(self):
        return self.__grade_id

    def set_grade_id(self, value):
        self.__grade_id = value


    def get_discipline_id(self):
        return self.__discipline_id

    def set_discipline_id(self, discipline_id):
        self.__discipline_id = discipline_id


    def get_student_id(self):
        return self.__student_id

    def set_student_id(self, student_id):
        self.__student_id = student_id


    def get_grade(self):
        return self.__grade_value

    def set_grade(self, grade_value):
        self.__grade_value = grade_value
