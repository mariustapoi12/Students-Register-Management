from src.domain.student_validator import  *
from src.domain.discipline_validator import *
from src.repository.discipline_repo import DisciplineRepository
from src.repository.grade_repo import *
from src.repository.student_repo import StudRepository
from src.services.gradeService import *
from src.services.statisticsService import *
from src.services.disciplineService import *
from src.ui.ui import *
import unittest
from src.undo_redo.undo_redo_repository import UndoRedoRepository
from src.undo_redo.undo_redo_service import UndoRedoService


class DisciplineClassTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_get_id(self):
        discipline = Discipline(1, "Math")
        self.assertEqual(discipline.get_discipline_id(), 1)

    def test_set_id(self):
        discipline = Discipline(1, "Math")
        discipline.set_discipline_id(3)
        self.assertEqual(discipline.get_discipline_id(), 3)

    def test_get_name(self):
        discipline = Discipline(1, "Math")
        self.assertEqual(discipline.get_name(), "Math")

    def test_set_name(self):
        discipline = Discipline(1, "Math")
        discipline.set_name("Algebra")
        self.assertEqual(discipline.get_name(), "Algebra")


class GradeClassTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_get_id(self):
        grade = Grade(1, 2, 3, 10)
        self.assertEqual(grade.get_grade_id(), 1)

    def test_set_id(self):
        grade = Grade(1, 2, 3,  10)
        grade.set_grade_id(3)
        self.assertEqual(grade.get_grade_id(), 3)

    def test_smth(self):
        grade = Grade(1, 2, 3, 10)
        grade.set_discipline_id(1)
        self.assertEqual(grade.get_discipline_id(), 1)

    def test_get_discipline_id(self):
        grade = Grade(1, 2, 3, 10)
        self.assertEqual(grade.get_discipline_id(), 3)

    def test_get_student_id(self):
        grade = Grade(1, 2, 3, 10)
        self.assertEqual(grade.get_student_id(), 2)

    def test_set_discipline_id(self):
        grade = Grade(1, 2, 3, 10)
        grade.set_student_id(100)
        self.assertEqual(grade.get_student_id(), 100)

    def test_get_grade(self):
        grade = Grade(1, 2, 3, 10)
        self.assertEqual(grade.get_grade(), 10)

    def test_set_grade(self):
        grade = Grade(1, 2, 3, 10)
        grade.set_grade(5)
        self.assertEqual(grade.get_grade(), 5)

class StudentClassTest(unittest.TestCase):
    def test_set_name(self):
        student = Student(1, "PCLB")
        student.set_name("Ondras")
        self.assertEqual(student.get_name(),"Ondras")

    def test_set_id(self):
        student = Student(1, "PCLB")
        student.set_student_id(10)
        self.assertEqual(student.get_student_id(), 10)


class StudentValidatorTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_validate_good_id_validates(self):
        student = Student(1, "Tudor")
        StudentValidator.validate(self, student)
        self.assertIsInstance(student.get_student_id(), int)

    def test_validate_negative_id_raisesStudentValidatorException(self):
        student = Student(-100, "Tudy")
        with self.assertRaises(StudentValidatorException):
            StudentValidator.validate(self, student)

    def test_validate_non_integer_id_raisesStudentValidatorException(self):
        student = Student("111dadada", "Tudy")
        with self.assertRaises(StudentValidatorException):
            StudentValidator.validate(self, student)


class DisciplineValidatorTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_validate_good_id_validates(self):
        discipline = Discipline(1, "Math")
        DisciplineValidator.validate(self, discipline)
        self.assertIsInstance(discipline.get_discipline_id(), int)

    def test_validate_negative_id_raisesStudentValidatorException(self):
        discipline = Discipline(-100, "Yes")
        with self.assertRaises(DisciplineValidatorException):
            DisciplineValidator.validate(self, discipline)


class GradeValidatorTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_validate_good_id_validates(self):
        grade = Grade(1, 2, 3, 10)
        GradeValidator.validate(self, grade)
        self.assertIsInstance(grade.get_grade_id(), int)
        self.assertIsInstance(grade.get_student_id(), int)
        self.assertIsInstance(grade.get_discipline_id(), int)
        self.assertIsInstance(grade.get_grade(), int)

    def test_validate_negative_student_id_raisesGradeValidatorException(self):
        grade = Grade(1, -2, 3, 10)
        with self.assertRaises(GradeValidatorException):
            GradeValidator.validate(self, grade)

    def test_validate_negative_discipline_id_raisesGradeValidatorException(self):
        grade = Grade(1, 2, -3, 10)
        with self.assertRaises(GradeValidatorException):
            GradeValidator.validate(self, grade)

    def test_validate_negative_grade_value_raisesGradeValidatorException(self):
        grade = Grade(1, 2, 3, -10)
        with self.assertRaises(GradeValidatorException):
            GradeValidator.validate(self, grade)

    def test_validate_higher_grade_value_raisesGradeValidatorException(self):
        grade = Grade(1, 2, 3, 20)
        with self.assertRaises(GradeValidatorException):
            GradeValidator.validate(self, grade)

    def test_validate_non_integer_student_id_raisesGradeValidatorException(self):
        grade = Grade(2, "123t", 3, 10)
        with self.assertRaises(GradeValidatorException):
            GradeValidator.validate(self, grade)

    def test_validate_non_integer_discipline_id_raisesGradeValidatorException(self):
        grade = Grade(2, 3, "123t", 10)
        with self.assertRaises(GradeValidatorException):
            GradeValidator.validate(self, grade)

    def test_validate_non_integer_grade_value_raisesGradeValidatorException(self):
        grade = Grade(1, 2, 3, "123t")
        with self.assertRaises(GradeValidatorException):
            GradeValidator.validate(self, grade)

class DisciplineServiceTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generate_random_disciplines(self):
        undo_redo_repository = UndoRedoRepository()
        discipline_validator = DisciplineValidator
        discipline_repository = DisciplineRepository(discipline_validator)
        discpiline_service = DisciplineService(discipline_repository, undo_redo_repository)
        discpiline_service.generate_random_disciplines()
        self.assertEqual(discpiline_service.get_repo_data_length(), 10)

    def test_add_discipline(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        discipline_validator = DisciplineValidator
        discipline_repository = DisciplineRepository(discipline_validator)
        discipline_service = DisciplineService(discipline_repository, undo_redo_service)
        discipline = "Math"
        discipline_id = 1
        discipline_service.add_discipline(discipline_id, discipline)
        self.assertIn(discipline_id, discipline_service.get_repo_data())

    def test_remove_discpline(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        discipline_validator = DisciplineValidator
        discipline_repository = DisciplineRepository(discipline_validator)
        discipline_service = DisciplineService(discipline_repository, undo_redo_service)
        discipline = "Math"
        discipline_id = 1
        operatations = []
        discipline_service.add_discipline(discipline_id, discipline)
        discipline_service.remove_discipline(discipline_id, operatations)
        self.assertNotIn(discipline_id, discipline_service.get_repo_data())

    def test_update_discipline(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        discipline_validator = DisciplineValidator
        discipline_repository = DisciplineRepository(discipline_validator)
        discipline_service = DisciplineService(discipline_repository, undo_redo_service)
        discipline = "Math"
        discipline_id = 1
        discipline_service.add_discipline(discipline_id, discipline)
        discipline_service.update_discipline(discipline_id, "Algebra")
        self.assertIn(discipline_id, discipline_service.get_repo_data())

    def test_display_disciplines(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        discipline_validator = DisciplineValidator
        discipline_repository = DisciplineRepository(discipline_validator)
        discipline_service = DisciplineService(discipline_repository, undo_redo_service)
        discipline = "Math"
        discipline_id = 1
        discipline_service.add_discipline(discipline_id, discipline)
        list = [[discipline_id, discipline]]
        self.assertEqual(discipline_service.display_disciplines(), list)

    def test_search_disciplines_by_id(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        discipline_validator = DisciplineValidator
        discipline_repository = DisciplineRepository(discipline_validator)
        discipline_service = DisciplineService(discipline_repository, undo_redo_service)
        discipline1 = "Math"
        discipline_id1 = "1"
        discipline_service.add_discipline(discipline_id1, discipline1)
        discipline2 = "FP"
        discipline_id2 = "11"
        discipline_service.add_discipline(discipline_id2, discipline2)
        list = [[int(discipline_id1), discipline1], [int(discipline_id2), discipline2]]
        self.assertEqual(discipline_service.search_disciplines_by_id(discipline_id1), list)

    def test_search_disciplines_by_name(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        discipline_validator = DisciplineValidator
        discipline_repository = DisciplineRepository(discipline_validator)
        discipline_service = DisciplineService(discipline_repository, undo_redo_service)
        discipline1 = "Python2"
        discipline_id1 = 1
        discipline_service.add_discipline(discipline_id1, discipline1)
        discipline2 = "Python3"
        discipline_id2 = 2
        discipline_service.add_discipline(discipline_id2, discipline2)
        list = [[int(discipline_id1), discipline1], [int(discipline_id2), discipline2]]
        self.assertEqual(discipline_service.search_disciplines_by_name("Python"), list)

class StudentServiceTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_discipline(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        student_validator = StudentValidator
        student_repository = StudRepository(student_validator)
        student_service = StudentService(student_repository, undo_redo_service)
        student = "Math"
        student_id = 1
        student_service.add_student(student_id, student)
        self.assertIn(student_id, student_service.get_repo_data())

    def test_generate_random_students(self):
        undo_redo_repository = UndoRedoRepository()
        student_validator = StudentValidator
        student_repository = StudRepository(student_validator)
        student_service = StudentService(student_repository, undo_redo_repository)
        student_service.generate_random_students()
        self.assertEqual(student_service.get_repo_data_length(), 10)

    def test_remove_student(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        student_validator = StudentValidator
        student_repository = StudRepository(student_validator)
        student_service = StudentService(student_repository, undo_redo_service)
        student = "Math"
        student_id = 1
        operatations = []
        student_service.add_student(student_id, student)
        student_service.remove_student(student_id, operatations)
        self.assertNotIn(student_id, student_service.get_repo_data())

    def test_update_student(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        student_validator = StudentValidator
        student_repository = StudRepository(student_validator)
        student_service = StudentService(student_repository, undo_redo_service)
        student = "Math"
        student_id = 1
        student_service.add_student(student_id, student)
        student_service.update_student(student_id, "Algebra")
        self.assertIn(student_id, student_service.get_repo_data())

    def test_display_students(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        student_validator = StudentValidator
        student_repository = StudRepository(student_validator)
        student_service = StudentService(student_repository, undo_redo_service)
        student = "Math"
        student_id = 1
        student_service.add_student(student_id, student)
        list = [[student_id, student]]
        self.assertEqual(student_service.display_students(), list)

    def test_search_students_by_id(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        student_validator = StudentValidator
        student_repository = StudRepository(student_validator)
        student_service = StudentService(student_repository, undo_redo_service)
        student1 = "Math"
        student_id1 = "1"
        student_service.add_student(student_id1, student1)
        student2 = "FP"
        student_id2 = "11"
        student_service.add_student(student_id2, student2)
        list = [[int(student_id1), student1], [int(student_id2), student2]]
        self.assertEqual(student_service.search_students_by_id(student_id1), list)

    def test_search_students_by_name(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        student_validator = StudentValidator
        student_repository = StudRepository(student_validator)
        student_service = StudentService(student_repository, undo_redo_service)
        student1 = "Python2"
        student_id1 = 1
        student_service.add_student(student_id1, student1)
        student2 = "Python3"
        student_id2 = 2
        student_service.add_student(student_id2, student2)
        list = [[int(student_id1), student1], [int(student_id2), student2]]
        self.assertEqual(student_service.search_students_by_name("Python"), list)

class GradeServiceTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generate_random_grades(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        grade_validator = GradeValidator
        grade_repoistory = GradeRepository(grade_validator)
        grade_service = GradeService(grade_repoistory, undo_redo_service)
        grade_service.generate_random_grades()
        self.assertEqual(grade_service.get_repo_data_length(), 20)

    def test_add_grade(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        grade_validator = GradeValidator
        grade_repoistory = GradeRepository(grade_validator)
        grade_service = GradeService(grade_repoistory, undo_redo_service)
        grade_id = 0
        student_id = 1
        discipline_id = 1
        grade_value = 10
        grade_service.add_grade(grade_id, student_id, discipline_id, grade_value)
        self.assertEqual(grade_service.get_repo_data_length(), 1)

    def test_remove_grades_student(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        grade_validator = GradeValidator
        grade_repoistory = GradeRepository(grade_validator)
        grade_service = GradeService(grade_repoistory, undo_redo_service)
        operations = []
        grade_id = 0
        student_id = 1
        discipline_id = 1
        grade_value = 10
        grade_service.add_grade(grade_id, student_id, discipline_id, grade_value)
        grade_service.add_grade(grade_id, student_id, discipline_id, grade_value)
        self.assertEqual(grade_service.get_repo_data_length(), 2)
        grade_service.remove_grades_student(student_id, operations)
        self.assertEqual(grade_service.get_repo_data_length(), 0)

    def test_remove_disciplines_grades(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        grade_validator = GradeValidator
        grade_repoistory = GradeRepository(grade_validator)
        grade_service = GradeService(grade_repoistory, undo_redo_service)
        operations = []
        grade_service.add_grade(1, 1, 1, 10)
        grade_service.add_grade(2, 2, 1, 9)
        self.assertEqual(grade_service.get_repo_data_length(), 2)
        grade_service.remove_disciplines_grades(1, operations)
        self.assertEqual(grade_service.get_repo_data_length(), 0)

    def test_display_grades(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        grade_validator = GradeValidator
        grade_repoistory = GradeRepository(grade_validator)
        grade_service = GradeService(grade_repoistory, undo_redo_service)
        grade_service.add_grade(1, 1, 1, 10)
        grade_service.add_grade(2, 2, 1, 9)
        self.assertEqual(grade_service.display_grades(),[[1, 1, 1, 10],[2, 2, 1, 9]])

    def test_get_repo_data(self):
        undo_redo_repository = UndoRedoRepository()
        undo_redo_service = UndoRedoService(undo_redo_repository)
        grade_validator = GradeValidator
        grade_repoistory = GradeRepository(grade_validator)
        grade_service = GradeService(grade_repoistory, undo_redo_service)
        self.assertEqual(grade_service.get_repo_data(), {})

class StatisticsServiceTest (unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calculate_who_and_how_many_are_failing(self):
        studentsList = [[1, "Andrei"],[2, "Marius"], [3, "Flaviu"]]
        disciplinesList = [[1,"Python"],[2, "Algebra"]]
        gradesList = [[1, 1, 1, 10],[2, 1, 1, 8], [3, 3, 1, 4], [4, 1, 2, 2], [5, 2, 2, 5], [6, 3, 2, 1]]
        statistics_serivce = StatisticsService(studentsList, disciplinesList, gradesList)
        self.assertEqual(statistics_serivce.calculate_who_and_how_many_are_failing(), (66, [[1, 'Andrei'], [3, 'Flaviu']]))

    def test_calculate_students_with_the_best_situation(self):
        studentsList = [[1, "Andrei"], [2, "Marius"], [3, "Flaviu"]]
        disciplinesList = [[1, "Python"], [2, "Algebra"]]
        gradesList = [[1, 1, 1, 5], [2, 2, 1, 8], [3, 3, 1, 4], [4, 1, 2, 6], [5, 2, 2, 5], [6, 3, 2, 1]]
        statistics_serivce = StatisticsService(studentsList, disciplinesList, gradesList)
        self.assertEqual(statistics_serivce.calculate_students_with_the_best_situation(),
                         (66, [[2, 'Marius'], [1, 'Andrei']]))

    def test_calculate_graded_disciplines_statistic(self):
        studentsList = [[1, "Andrei"], [2, "Marius"], [3, "Flaviu"]]
        disciplinesList = [[1, "Python"], [2, "Algebra"]]
        gradesList = [[1, 1, 1, 5], [2, 2, 1, 8], [3, 3, 1, 4], [4, 1, 2, 6], [5, 2, 2, 5], [6, 3, 2, 10]]
        statistics_serivce = StatisticsService(studentsList, disciplinesList, gradesList)
        self.assertEqual(statistics_serivce.calculate_graded_disciplines_statistic(), (100, [[2, 'Algebra'], [1, 'Python']]))

    def test_is_student_failing_return_true(self):
        studentsList = [[1, "Andrei"], [2, "Marius"], [3, "Flaviu"]]
        disciplinesList = [[1, "Python"], [2, "Algebra"]]
        gradesList = [[1, 1, 1, 10], [3, 3, 1, 4], [4, 1, 2, 2],  [6, 3, 2, 1]]
        statistics_serivce = StatisticsService(studentsList, disciplinesList, gradesList)
        self.assertEqual(statistics_serivce.calculate_who_and_how_many_are_failing(),
                         (100, [[1, 'Andrei'], [2, 'Marius'], [3, 'Flaviu']]))

    def test_calculate_studentsDictionary_returns_none(self):
        studentsList = []
        disciplinesList = []
        gradesList = []
        statistics_serivce = StatisticsService(studentsList, disciplinesList, gradesList)
        self.assertEqual(statistics_serivce.calculate_studentsDictionary(), None)