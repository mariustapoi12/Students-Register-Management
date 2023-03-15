class DisciplineValidatorException(Exception):
    pass

class DisciplineValidator:
    def validate(self, discipline):
        """
        Validates the discipline object
        Raises exception if the id is negative
        """
        if int(discipline.get_discipline_id()) < 0:
            raise DisciplineValidatorException("The id must be positive")