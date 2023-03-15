from src.services.disciplineService import *
from src.services.studentService import *


class StatisticsService:
    def __init__(self, studentsList, disciplinesLists, gradesList):
        self._grades_list = {}
        for grade in gradesList:
            self._grades_list[grade[0]] = grade

        self._students_list = {}
        for student in studentsList:
            self._students_list[student[0]] = student

        self._disciplines_list = {}
        for discipline in disciplinesLists:
            self._disciplines_list[discipline[0]] = discipline

    def is_student_failing(self, student, studentsDictionary):
        student_has_grades = False
        if student[0] in list(studentsDictionary.keys()):
            for discipline_id in list(studentsDictionary[student[0]].keys()):
                    sum_of_grades = studentsDictionary[student[0]][discipline_id]
                    number_of_grades = int((sum_of_grades * 10) % 10)
                    sum_of_grades = int((sum_of_grades * 10) / 10)
                    average_grade = int(sum_of_grades / number_of_grades)
                    student_has_grades = True
                    if average_grade < 5:
                        return True
        if student_has_grades:
            return False
        else:
            return True


    def calculate_students_gradeDictionary(self, student):
        gradesDictionary = {} # gradesDictionary[discipline_id] = average_grade + number_of_grades
        for grade_index in self._grades_list:
            grade = self._grades_list[grade_index] #[grade_id, student_id, discipline_id, grade]
            if grade[1] == student[0]:
                if grade[2] not in gradesDictionary:
                    gradesDictionary[grade[2]] = grade[3]
                    gradesDictionary[grade[2]] += 0.1
                else:
                    gradesDictionary[grade[2]] += grade[3]
                    gradesDictionary[grade[2]] += 0.1
        return gradesDictionary

    def calculate_students_averagesDictionary(self):
        studentsDictionary = self.calculate_studentsDictionary()
        averagesDictionary = {}
        for student_index in self._students_list:
            student = self._students_list[student_index]
            gradesDictionary = self.calculate_students_gradeDictionary(student)
            sum_of_average_grades = 0
            number_of_disciplines = 0
            for discipline_id in list(gradesDictionary.keys()):
                sum_of_grades = gradesDictionary[discipline_id]
                number_of_grades = int((sum_of_grades * 10) % 10)
                sum_of_grades = int((sum_of_grades * 10) / 10)
                average_grade = int(sum_of_grades / number_of_grades)

                sum_of_average_grades = sum_of_average_grades + average_grade
                number_of_disciplines = number_of_disciplines + 1
            if number_of_disciplines > 0:
                average_of_average_grades = sum_of_average_grades / number_of_disciplines
                averagesDictionary[student[0]] = average_of_average_grades
        return averagesDictionary

    def calculate_studentsDictionary(self):
        # studentsDictionary[student.id] = gradesDictionary
        studentsDictionary = {}
        for student_index in self._students_list:
            student = self._students_list[student_index]
            gradesDictionary = self.calculate_students_gradeDictionary(student)
            if len(gradesDictionary) > 0:
                studentsDictionary[student[0]] = gradesDictionary
        if len(studentsDictionary) > 0:
            return studentsDictionary
        else:
            return None

    def calculate_who_and_how_many_are_failing(self):
        studentsDictionary = {}
        studentsDictionary = self.calculate_studentsDictionary()
        failingNumber = 0
        studentsNumber = 0
        failsList = []
        for student_index in self._students_list:
            student = self._students_list[student_index]
            if len(studentsDictionary) > 0:
                if self.is_student_failing(student, studentsDictionary) == True:
                    failsList.append(student)
                    failingNumber = failingNumber + 1
            studentsNumber = studentsNumber + 1

        failingPercentage = int(failingNumber * 100 / studentsNumber)
        return failingPercentage, failsList

    def calculate_who_and_how_many_are_passing(self):
        studentsDictionary = {}
        studentsDictionary = self.calculate_studentsDictionary()
        passingStudentsNumber = 0
        studentsNumber = 0
        passingStudentsList = []
        for student_index in self._students_list:
            student = self._students_list[student_index]
            if len(studentsDictionary) > 0:
                if self.is_student_failing(student, studentsDictionary) == False:
                    passingStudentsList.append(student)
                    passingStudentsNumber = passingStudentsNumber + 1
            studentsNumber = studentsNumber + 1

        passingPercentage = int(passingStudentsNumber * 100 / studentsNumber)
        return passingPercentage, passingStudentsList

    def calculate_students_with_the_best_situation(self):
        studentsDictionary = self.calculate_studentsDictionary()
        passingPercentage, passingStudentsList = self.calculate_who_and_how_many_are_passing()
        self.sort_students_descending_by_grade(passingStudentsList)
        return passingPercentage, passingStudentsList

    def sort_students_descending_by_grade(self, passingStudentsList):
        studentsDictionary = self.calculate_studentsDictionary()
        averagesDictionary = self.calculate_students_averagesDictionary()
        for first_student in passingStudentsList:
            for second_student in passingStudentsList:
                if int(averagesDictionary[first_student[0]]) > int(averagesDictionary[second_student[0]]):
                    auxiliar_student = Student(second_student[0], second_student[1])
                    second_student[0] = (first_student[0])
                    second_student[1] = (first_student[1])
                    first_student[0] = auxiliar_student.get_student_id()
                    first_student[1] = (auxiliar_student.get_name())
                    # first_student, second_student = second_student, first_student

    def calculate_which_and_how_many_disciplines_are_graded(self):
        averagesDictionary = self.calculate_disciplines_averagesDictionary()
        gradedDisciplines = 0
        disciplinesNumber = 0
        gradedDisciplinesList = []
        for discipline_index in self._disciplines_list:
            discipline = self._disciplines_list[discipline_index]
            if discipline[0] in list(averagesDictionary.keys()):
                gradedDisciplinesList.append(discipline)
                gradedDisciplines = gradedDisciplines + 1
            disciplinesNumber = disciplinesNumber + 1

        gradedPercentage = int(gradedDisciplines * 100 / disciplinesNumber)
        return gradedPercentage, gradedDisciplinesList

    def calculate_disciplineDictionary(self):
        disciplinesDictionary = {}  # disciplinesDictionary[discipline_id] = DG
        # DG[Student_id] = average_grade
        studentsDictionary = self.calculate_studentsDictionary()
        for student_id in list(studentsDictionary.keys()):
            gradesDictionary = studentsDictionary[student_id]
            for discipline_id in list(gradesDictionary.keys()):
                grade_value = gradesDictionary[discipline_id]
                number_of_grades = (grade_value * 10) % 10
                grade_value = grade_value * 10
                grade_value = int(grade_value / 10)
                average_grade = int(grade_value / number_of_grades)
                if discipline_id not in list(disciplinesDictionary.keys()):
                    disciplinesDictionary[discipline_id] = average_grade + 0.1
                else:
                    disciplinesDictionary[discipline_id] = disciplinesDictionary[discipline_id] + average_grade + 0.1
        return disciplinesDictionary

    def sort_disciplines_descending_by_grade(self):
        averagesDictionary = self.calculate_disciplines_averagesDictionary()
        gradedPercentage, gradedDisciplinesList = self.calculate_which_and_how_many_disciplines_are_graded()
        for first_discipline in gradedDisciplinesList:
            for second_discipline in gradedDisciplinesList:
                if int(averagesDictionary[first_discipline[0]]) > int(
                        averagesDictionary[second_discipline[0]]):
                    auxiliar_discipline = Discipline(second_discipline[0], second_discipline[1])
                    second_discipline[0] = (first_discipline[0])
                    second_discipline[1] = (first_discipline[1])
                    first_discipline[0] = auxiliar_discipline.get_discipline_id()
                    first_discipline[1] = (auxiliar_discipline.get_name())

    def calculate_disciplines_averagesDictionary(self):
        disciplinesDictionary = self.calculate_disciplineDictionary()
        averagesDictionary = {}
        for discipline_id in list(disciplinesDictionary.keys()):
            sum_of_grades = disciplinesDictionary[discipline_id]
            number_of_students = int((sum_of_grades * 10) % 10)
            sum_of_grades = int((sum_of_grades * 10) / 10)
            if number_of_students > 0:
                average_of_grades = int(sum_of_grades / number_of_students)
                averagesDictionary[discipline_id] = average_of_grades
        return averagesDictionary

    def calculate_graded_disciplines_statistic(self):
        averagesDictionary = self.calculate_disciplines_averagesDictionary()
        gradedPercentage, gradedDisciplinesList = self.calculate_which_and_how_many_disciplines_are_graded()
        self.sort_disciplines_descending_by_grade()
        return gradedPercentage, gradedDisciplinesList
