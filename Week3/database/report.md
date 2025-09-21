#Table Students
student(student_id, class_id, name, email)

#Table Lecturers
lecturer(lecturer_id, student_id, lecturer_name, subject_id)

#Table Classes
class(class_id, description)

#Table Subjects
subjects(subject_id, class_id, subject_name)