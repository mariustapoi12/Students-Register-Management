from src.ui.ui import *
from src.domain.discipline import *
from src.domain.grade import *
from src.domain.student import *
from src.domain.student_validator import *
from src.domain.grade_validator import *
from src.domain.discipline_validator import *
from src.repository.discipline_repo import *
from src.repository.grade_repo import *
from src.repository.student_repo import *
from src.services.gradeService import *
from src.services.disciplineService import *
from src.services.studentService import *
from src.services.statisticsService import *
from src.undo_redo.undo_redo import *
from src.undo_redo.undo_redo_repository import *
from src.undo_redo.undo_redo_service import *

student_validator = StudentValidator
discipline_validator = DisciplineValidator
grade_validator = GradeValidator

"""
repository = inmemory

repository = textfiles
students = students.txt
disciplines = disciplines.txt
grades = grades.txt

repository = binaryfiles
students = students_pickle.bin
disciplines = disciplines_pickle.bin
grades = grades_pickle.bin
"""

settings_file = open("settings.properties", "rt")
count = 0
for line in settings_file.readlines():
    name, option = line.split(maxsplit=1, sep=' = ')
    option = option.strip()
    count += 1
    if count ==1:
        saved_option = option
        if option == "inmemory":
            student_repository = StudRepository(student_validator)
            discipline_repository = DisciplineRepository(discipline_validator)
            grade_repository = GradeRepository(grade_validator)
            break
        else:
            std_repository = StudRepository(student_validator)
            dsp_repository = DisciplineRepository(discipline_validator)
            grd_repository = GradeRepository(grade_validator)
    if count == 2:
        if saved_option =="textfiles":
            student_repository = StudentTextFileRepository(option)
        else:
            student_repository = StudentBinFileRepository(option)
    if count == 3:
        if saved_option == "textfiles":
            discipline_repository = DisciplineTextFileRepository(option)
        else:
            discipline_repository = DisciplineBinFileRepository(option)
    if count == 4:
        if saved_option == "textfiles":
            grade_repository = GradeTextFileRepository(option)
        else:
            grade_repository = GradeBinFileRepository(option)
settings_file.close()

"""student_repository = StudRepository(student_validator)
discipline_repository = DisciplineRepository(discipline_validator)
grade_repository = GradeRepository(grade_validator)"""
undo_redo_repository = UndoRedoRepository()

undo_redo_service = UndoRedoService(undo_redo_repository)
student_service = StudentService(student_repository, undo_redo_service)
discipline_service = DisciplineService(discipline_repository, undo_redo_service)
grade_service = GradeService(grade_repository, undo_redo_service)
if saved_option != "textfiles":
    student_service.generate_random_students()
    discipline_service.generate_random_disciplines()
    grade_service.generate_random_grades()
statistics_service = StatisticsService(student_service.display_students(),
                                      discipline_service.display_disciplines(),
                                      grade_service.display_grades())

ui = RegisterUI(student_service, discipline_service, grade_service, statistics_service, undo_redo_service)
ui.start()