#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import argparse
import csv

# Функция для ввода данных о маршрутах
def add_route(conn, start, end, number):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO routes (start, end, number) VALUES (?, ?, ?)", (start, end, number))
    conn.commit()
    return cursor.lastrowid

# Функция для вывода информации о всех маршрутах в CSV
def export_to_csv(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT start, end, number FROM routes")
    routes = cursor.fetchall()

    with open("routes.csv", "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Start", "End", "Number"])  # Заголовки столбцов

        for route in routes:
            csv_writer.writerow(route)

# Функция для вывода информации о маршруте по номеру
def find_route(conn, number):
    cursor = conn.cursor()
    cursor.execute("SELECT start, end FROM routes WHERE number = ?", (number,))
    result = cursor.fetchone()

    if result:
        return result
    else:
        return None

if __name__ == '__main__':
    # Создаем соединение с базой данных
    conn = sqlite3.connect("idz.db")

    # Создаем таблицу routes, если она еще не существует
    conn.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start TEXT,
            end TEXT,
            number TEXT
        )
    ''')

    parser = argparse.ArgumentParser(description='Управление маршрутами')
    parser.add_argument('--add', action='store_true', help='Добавить новый маршрут')
    parser.add_argument('--number', type=str, help='Номер маршрута для поиска')
    parser.add_argument('--export', action='store_true', help='Экспортировать все маршруты в CSV')

    args = parser.parse_args()

    if args.add:
        start = input("Введите начальный пункт маршрута: ")
        end = input("Введите конечный пункт маршрута: ")
        number = input("Введите номер маршрута: ")
        added_id = add_route(conn, start, end, number)
        print(f"Маршрут с ID {added_id} добавлен.")

    if args.export:
        export_to_csv(conn)
        print("Маршруты экспортированы в CSV.")

    if args.number:
        result = find_route(conn, args.number)
        if result:
            print("Начальный пункт маршрута:", result[0])
            print("Конечный пункт маршрута:", result[1])
        else:
            print("Маршрут с таким номером не найден.")

    # Закрываем соединение с базой данных
    conn.close()
