#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import unittest

from idz21 import add_route, find_route


class TestRoutesDatabase(unittest.TestCase):
    def setUp(self):
        # Создаем временное соединение с базой данных
        self.conn = sqlite3.connect(":memory:")
        # Создаем таблицу routes для тестов, если она еще не существует
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start TEXT,
                end TEXT,
                number TEXT
            )
        ''')

    def test_add_route(self):
        add_route(self.conn, "Start1", "End1", "1")
        # Проверяем, что маршрут действительно добавлен
        cursor = self.conn.cursor()
        cursor.execute("SELECT start, end, number FROM routes")
        routes = cursor.fetchall()
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0], ("Start1", "End1", "1"))

    def test_find_route(self):
        add_route(self.conn, "Start2", "End2", "2")
        # Проверяем, что можем найти маршрут по номеру
        result = find_route(self.conn, "2")
        self.assertEqual(result, ("Start2", "End2"))

    def tearDown(self):
        # Закрываем временное соединение с базой данных
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
