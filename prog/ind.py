#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import jsonschema

# JSON схема
schema = {
    "type": "object",
    "properties": {
        "full_name": {"type": "string"},
        "group_number": {"type": "string"},
        "grades": {"type": "array", "items": {"type": "number"}},
    },
    "required": ["full_name", "group_number", "grades"],
}


def add_student(students):
    full_name = input("Фамилия и инициалы? ")
    group_number = input("Номер группы? ")
    grades_str = input("Успеваемость (через пробел)? ")

    grades = [float(grade) for grade in grades_str.split()]

    student = {
        "full_name": full_name,
        "group_number": group_number,
        "grades": grades,
    }

    students.append(student)
    students.sort(key=lambda item: item.get("group_number", ""))


def list_students(students):
    line = "+-{}-+-{}-+-{}-+".format("-" * 30, "-" * 15, "-" * 20)
    print(line)
    print(
        "| {:^30} | {:^15} | {:^20} |".format("Ф.И.О.", "Номер группы", "Успеваемость")
    )
    print(line)

    for student in students:
        average_grade = sum(student.get("grades", 0)) / len(student.get("grades", 1))
        if average_grade > 4.0:
            print(
                "| {:<30} | {:<15} | {:<20} |".format(
                    student.get("full_name", ""),
                    student.get("group_number", ""),
                    ", ".join(map(str, student.get("grades", []))),
                )
            )
    print(line)


def help_command():
    print("Список команд:\n")
    print("add - добавить студента;")
    print("list - вывести список студентов;")
    print("save - сохранить данные в файл JSON;")
    print("load - загрузить данные из файла JSON;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")


def save_to_json(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_from_json(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


def validate_data(data):
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"Ошибка валидации: {e}")
        return False


def save_command(students):
    filename = input("Введите имя файла для сохранения данных: ")
    save_to_json(filename, students)
    print(f"Данные успешно сохранены в файл {filename}")


def load_command(students):
    filename = input("Введите имя файла для загрузки данных: ")
    loaded_data = load_from_json(filename)
    if validate_data(loaded_data):
        students.clear()
        students.extend(loaded_data)
        print(f"Данные успешно загружены из файла {filename}")
    else:
        print("Загруженные данные не прошли валидацию")


def main():
    students = []

    while True:
        command = input(">>> ").lower()

        if command == "exit":
            break
        elif command == "add":
            add_student(students)
        elif command == "list":
            list_students(students)
        elif command == "save":
            save_command(students)
        elif command == "load":
            load_command(students)
        elif command == "help":
            help_command()
        else:
            print(f"Неизвестная команда {command}")


if __name__ == "__main__":
    main()
