#!/usr/bin/env python3
import os
import sys
import populate
from flask import g
from flask import Flask, current_app
from flask import render_template, request, jsonify
import pymysql


app = Flask(__name__)
username = "root"
password = "root"
database = "hw5_ex2"

# This method returns a list of messages in a json format such as
# [
# { "name": <name>, "message": <message> },
# { "name": <name>, "message": <message> },
# ...
# ]
# If this is a POST request and there is a parameter "name" given, then only
# messages of the given name should be returned.
# If the POST parameter is invalid, then the response code must be 500.
@app.route("/messages", methods=["GET", "POST"])
def messages():
    with db.cursor() as cursor:
        # Create the base SQL query
        sql = "SELECT DISTINCT name, message FROM messages"

        # Make the query if there are no arguments
        if request.method == "GET":
            cursor.execute(sql)
            rows = cursor.fetchall()
            return jsonify(rows), 200        

        # Get the name and return 500 if name is absent
        name = request.form.get('name')
        if not name:
            return "Invalid input", 500

        # Add the name to the query, using a prepared statement
        sql += " WHERE name=%s"
        cursor.execute(sql, name)

        # Get the result and return them
        rows = cursor.fetchall()
        return jsonify(rows), 200


# This method returns the list of users in a json format such as
# { "users": [ <user1>, <user2>, ... ] }
# This methods should limit the number of users if a GET URL parameter is given
# named limit. For example, /users?limit=4 should only return the first four
# users.
# If the paramer given is invalid, then the response code must be 500.
@app.route("/users", methods=["GET"])
def contact():
    with db.cursor() as cursor:
        
        # Create the base query and get the result
        sql = "SELECT DISTINCT name FROM users"       
        cursor.execute(sql)
        results = cursor.fetchall()

        # Create a list of names from the query result
        users = [result["name"] for result in results]
        
        # Get the limit. If it is absent return everything
        limit = request.args.get('limit')
        if not limit:
            return jsonify({"users": users}), 200
        
        # Try transforming the limit to int
        try:
            # Transoform the limit to int
            limit = int(limit)
            
            # If limit is negative raise exeption
            if limit < 0:
                raise IndexError
            
            # Get the elements of the list until `limit`
            # and return the result
            limited_users = users[:limit]
            return jsonify({"users": limited_users}), 200

        # If `limit` is not an int, or it is bigger
        # than the total number of results return 500
        except (ValueError, IndexError):
            return "Invalid input", 500 
        

if __name__ == "__main__":
    seed = "randomseed"
    if len(sys.argv) == 2:
        seed = sys.argv[1]

    db = pymysql.connect("localhost",
                         username,
                         password,
                         database,
                         cursorclass=pymysql.cursors.DictCursor)
    with db.cursor() as cursor:
        populate.populate_db(seed, cursor)
        db.commit()
    print("[+] database populated")

    app.run(host='0.0.0.0', port=80)
