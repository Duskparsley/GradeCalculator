import matplotlib.pyplot as plt
import os

#get lists of student names
students_file = open('data/students.txt')
student_content = students_file.readlines()
student_names_id_dict = {}
for student in student_content:
    student_names_id_dict[student[3:][:-1]] = student[:3]

#get assignment list data
assignments_dict = {}
assignments_name_dict = {}
assignments_file = open('data/assignments.txt')
assignment_content = assignments_file.readlines()
for i in range(0, len(assignment_content), 3):
    assignments_dict[assignment_content[i+1][:-1]] = [assignment_content[i][:-1] , assignment_content[i+2][:-1]]
for i in range(0, len(assignment_content), 3):
    assignments_name_dict[assignment_content[i][:-1]] = [assignment_content[i+1][:-1], assignment_content[i+2][:-1]]


#unpack submissions
submission_stats_dict = {}
directory = r"C:\Users\ahmad\PycharmProjects\Lab_11\data\submissions"
for submission in os.scandir(directory):
    #open file
    submission_data = open(submission)
    #read first line in file
    submission_data = submission_data.readline()
    #index line values
    submission_data=submission_data.split("|")
    submission_student_id = submission_data[0]
    submission_assignment_id = submission_data[1]
    submission_grade = submission_data[2]
    #add to dict with key student id
    if submission_student_id not in submission_stats_dict:
        submission_stats_dict[submission_student_id] = [submission_assignment_id, submission_grade]
    #makes sure values arent overwritten
    submission_stats_dict[submission_student_id].append(submission_assignment_id)
    submission_stats_dict[submission_student_id].append(submission_grade)

def print_menu():
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    option = int(input("Enter your selection: "))
    if option == 1:
        option_1()
        exit()
    if option == 2:
        option_2()
        exit()
    if option == 3:
        option_3()
        exit()



def option_1():
    student = input("What is the student's name: ")
    if student not in student_names_id_dict:
        print("Student not found")
    studentId = student_names_id_dict[student]
    find_student_grade(studentId)

def option_2():
    assignment = input("What is the assignment name: ")
    if assignment not in assignments_name_dict:
        print("Assignment not found")
    assignmentId = assignments_name_dict[assignment][0]
    print(find_stats(assignmentId))

def find_stats(assignment_id):
    min_grade = 10000000
    max_grade = 0
    total_assignment_grade = 0
    for i in submission_stats_dict.values():
        for j in range(0, len(i), 2):
            if i[j] == assignment_id:
                total_assignment_grade += int(i[j+1])
                if int(i[j+1]) < min_grade:
                    min_grade = int(i[j+1])
                if int(i[j+1]) > max_grade:
                    max_grade = int(i[j+1])
                break
    assignment_average = total_assignment_grade / len(submission_stats_dict.keys())
    return [min_grade, max_grade, int(assignment_average)]

def option_3():
    scores_array = []
    assignment = input("What is the assignment name: ")
    if assignment not in assignments_name_dict:
        print("Assignment not found")
        return
    assignmentId = assignments_name_dict[assignment][0]
    for i in submission_stats_dict.values():
        for j in range(0, len(i), 2):
            if i[j] == assignmentId:
                scores_array.append(int(i[j + 1]))
                break
    plt.hist(scores_array)
    plt.show()

def find_student_grade(student_id):
    cumulative_grade = 0
    for i in range(0, len(submission_stats_dict[student_id]), 2):
        assignment_id = submission_stats_dict[student_id][i]
        student_score = submission_stats_dict[student_id][i+1]
        single_assignment_grade = float(assignments_dict[assignment_id][1]) * float(student_score)
        cumulative_grade += single_assignment_grade
        print(student_score)
        print(assignments_dict[assignment_id][1])
        print(single_assignment_grade)
        print(cumulative_grade)

    final_grade = cumulative_grade / 1000
    print(int(final_grade))

while True:
    print_menu()