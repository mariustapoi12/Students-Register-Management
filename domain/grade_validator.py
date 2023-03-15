class GradeValidatorException(Exception):
    pass

class GradeValidator:
    def validate(self, grade):
        """
        Validates the grade object
        Raises exception if the id is negative
        """
        try:
            student_id = int(grade.get_student_id())
            discipline_id = int(grade.get_discipline_id())
            grade_value = int(grade.get_grade())
        except Exception:
            raise GradeValidatorException("The values must be an integers")
        if student_id < 0 or discipline_id < 0 or grade_value < 0:
            raise GradeValidatorException("The ids must be positive")
        if grade_value > 10:
            raise GradeValidatorException("Grade can not be higher than 10")
