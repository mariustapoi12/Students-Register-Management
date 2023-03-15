from src.domain.discipline_validator import DisciplineValidatorException
from src.domain.grade_validator import GradeValidatorException
from src.domain.student_validator import StudentValidatorException
from src.repository.discipline_repo import DisciplineRepositoryException
from src.undo_redo.undo_redo_service import UndoRedoServiceException
from src.repository.grade_repo import GradeRepositoryException


class RegisterUI:
    def __init__(self, student_service, discipline_service, grade_service, statistics_service, undo_redo_service):
        self.__student_service = student_service
        self.__discipline_service = discipline_service
        self.__grade_service = grade_service
        self.__statistics_service = statistics_service
        self.__undo_redo_service = undo_redo_service

    def print_menu(self):
        print("1. Add a student")
        print("2. Remove a student")
        print("3. Update a student")
        print("4. Display all students")
        print("5. Add a discipline")
        print("6. Remove a discipline")
        print("7. Update a discipline")
        print("8. Display all disciplines")
        print("9. Grade student")
        print("10. Display grades and students")

        print("11. Search students")
        print("12. Search disciplines")
        print("13. Display all failing students")
        print("14. Display best students")
        print("15. Display best disciplines")

        print("16. Undo")
        print("17. Redo")

        print("18. Exit")

    def option1(self):
        id = int(input("Id: "))
        name = input("Name: ")
        self.__student_service.add_student(id, name)

    def option2(self):
        id = int(input("Id of the student you want to delete: "))
        operations = []
        self.__grade_service.remove_grades_student(id, operations)
        self.__student_service.remove_student(id, operations)

    def option3(self):
        id = int(input("Id of the student you want to update: "))
        new_name = input("Updated name: ")
        self.__student_service.update_student(id, new_name)

    def option4(self):
        list = self.__student_service.display_students()
        for i in list:
            print("ID:", i[0], " Name:", i[1])

    def option5(self):
        id = input("Id: ")
        name = input("Name: ")
        self.__discipline_service.add_discipline(id, name)

    def option6(self):
        id = int(input("Id of the discipline you want to delete: "))
        operations = []
        self.__grade_service.remove_disciplines_grades(id,operations)
        self.__discipline_service.remove_discipline(id, operations)

    def option7(self):
        id = int(input("Id of the student you want to update: "))
        new_name = input("Updated name: ")
        self.__discipline_service.update_discipline(id, new_name)

    def option8(self):
        list = self.__discipline_service.display_disciplines()
        for i in list:
            print("ID:", i[0], " Discipline:", i[1])

    def option9(self):
        grade_id = 0
        student_id = input("Id of the student you want to grade: ")
        discipline_id = input("Id of the discipline you want the student to be graded:")
        grade_value = input("Grade value:")
        self.__grade_service.add_grade(grade_id ,student_id, discipline_id, grade_value)

    def option10(self):
        list = self.__grade_service.display_grades()
        for i in list:
            print("StudentID: ", i[1], " DisciplineID: ", i[2], " Grade: ", i[3])

    def option11(self):
        option_chosen = int(input("Press 1 to search by id or press 2 to search by name: "))
        if option_chosen == 1:
            findid = int(input("ID: "))
            findid = str(findid)
            list = self.__student_service.search_students_by_id(findid)
            for i in list:
                print("ID:", i[0], " Name:", i[1])
        elif option_chosen == 2:
            findname = input("Name: ")
            list = self.__student_service.search_students_by_name(findname)
            for i in list:
                print("ID:", i[0], " Name:", i[1])
        else:
            print("Invalid option!")

    def option12(self):
        option_chosen = int(input("Press 1 to search by ID or press 2 to search by name: "))
        if option_chosen == 1:
            findid = int(input("ID: "))
            findid = str(findid)
            list = self.__discipline_service.search_disciplines_by_id(findid)
            for i in list:
                print("ID:", i[0], " Discipline:", i[1])
        elif option_chosen == 2:
            findname = input("Name: ")
            list = self.__discipline_service.search_disciplines_by_name(findname)
            for i in list:
                print("ID:", i[0], " Discipline:", i[1])
        else:
            print("Invalid option!")

    def option13(self):
        failingPercentage, failsList = self.__statistics_service.calculate_who_and_how_many_are_failing()
        print(failingPercentage)
        for i in failsList:
            print("StudentID: ", i[0], "Name: ", i[1])

    def option14(self):
        passingPercentage, passingList = self.__statistics_service.calculate_students_with_the_best_situation()
        print(passingPercentage)
        for i in passingList:
            print("StudentID: ", i[0], "Name: ", i[1])

    def option15(self):
        gradedPercentage, gradedList = self.__statistics_service.calculate_graded_disciplines_statistic()
        print(gradedPercentage)
        for i in gradedList:
            print("GradeID: ", i[0], "Discipline: ", i[1])

    def option16(self):
        self.__undo_redo_service.undo()

    def option17(self):
        self.__undo_redo_service.redo()

    def start(self):
        """self.__student_service.generate_random_students()
        self.__discipline_service.generate_random_disciplines()
        self.__grade_service.generate_random_grades()"""
        while True:
            self.print_menu()
            try:
                option = int(input("User option: "))
                if option == 1:
                    self.option1()
                elif option == 2:
                    self.option2()
                elif option == 3:
                    self.option3()
                elif option == 4:
                    self.option4()
                elif option == 5:
                    self.option5()
                elif option == 6:
                    self.option6()
                elif option == 7:
                    self.option7()
                elif option == 8:
                    self.option8()
                elif option == 9:
                    self.option9()
                elif option == 10:
                    self.option10()
                elif option == 11:
                    self.option11()
                elif option == 12:
                    self.option12()
                elif option == 13:
                    self.option13()
                elif option == 14:
                    self.option14()
                elif option == 15:
                    self.option15()
                elif option == 16:
                    self.option16()
                elif option == 17:
                    self.option17()
                elif option == 18:
                    return
                else:
                    print ("Invalid user option!")
            except ValueError as ve:
                print(str(ve))
            except StudentValidatorException as sve:
                print(str(sve))
            except DisciplineValidatorException as dve:
                print(str(dve))
            except GradeValidatorException as gve:
                print(str(gve))
            except UndoRedoServiceException as urse:
                print(str(urse))
            except DisciplineRepositoryException as dre:
                print(str(dre))
            except GradeRepositoryException as gre:
                print(str(gre))
            except AttributeError as ae:
                print(str(ae))