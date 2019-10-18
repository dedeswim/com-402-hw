#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql.cursors

# Connect to the database named "students" using "monty" as username
# and "python" as a password. Use a DictCursor.
connection = pymysql.connect(host='localhost',
                             user='monty',
                             password='python',
                             database='students',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    connection.commit()

    with connection.cursor() as cursor:
        # Read all records from the "grades" table and put the result into the
        # "result" variable.
        sql_read = "SELECT * FROM `grades`"
        cursor.execute(sql_read)
        result = cursor.fetchall()
        print(result)

        # Create a new record with the name "bryan" and a grade of 6.
        sql_write = "INSERT INTO `grades` (`name`, `grade`) VALUES (%s, %s)"
        cursor.execute(sql_write, ('bryan', 6))

        # Read all records again and put the result in the variable "result"
        cursor.execute(sql_read)
        result = cursor.fetchall()

        found = False
        for row in result:
            if row["name"] == "bryan" and int(row["grade"]) == 6:
                print("Victory is sweetest when you’ve known defeat.")
                found = True

        if not found:
            print(
                "I can only show you the door. You're the one that has to walk through it.")

finally:
    # Don't forget to close the connections !
    connection.close()
