Tech Stack used:
    Flask
    PostgreSQL
    HTML templates

To run the API 
    1.First make sure that you have postgreSQL setup and create database named "testdb" using psql commandline
    2.Change the username and password setting in app.CONFIG according to your credentials
    3.Run python model.py
    4.Run python manage.py db init
    5.Run python manage.py db migrate
    6.Finally run python app.py to start the API

Go to http://127.0.0.1:1234/upload or the path showing to you in command prompt once the app is running and then set got to path /upload

Enter the XML file and corresponding Image File and click Submit
The resulting image with bounding boxes will be displayed in the page and the details will be stored in SQL database

![alt text](https://github.com/Nathandrake229/BaggageAI_API/blob/main/Screenshot_(3).png?raw=true)

I used PostgreSQL database because it is a fully flexible SQL database and importantly it supports wide range of datatypes especially Datetime which was required for this assignment.

To get the csv result of the queries made between a start date and end date in the same path replace upload with retrieve and enter a start date and end date and hit submit. A CSV file will be downloaded. An example of that CSV is in the repo named as result(1).csv


Since each image can have multiple objects, i am storing each object in seperate row along with their source image name as it keeps the database simple and avoids cluttering and conflicts. Since each object has its own bounding box coordinates, its simple to keep each object in seperate rows in the table.
