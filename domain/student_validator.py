class StudentValidatorException(Exception):
    pass

class StudentValidator:
    def validate(self, student):
        """
        Validates the student object
        Raises exception if the id is negative
        """
        try:
            id = int(student.get_student_id())
        except Exception:
            raise StudentValidatorException("The id must be an integer")
        if id < 0:
            raise StudentValidatorException("The id must be positive")