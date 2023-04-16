# My First Web Application

This program was created as part of an assignment for a third year Computer Science paper at Massey University. 

This assignment was completed 16 April 2023.

## About the Assignment

In this assignment, you will extend the minimalistic Web servers developed in the exercises
from the lectures. Here you will develop a Web application to generate an online (and not
necessarily serious) psychological profile of the user.

Your application will function both as a server to the end user and as a client itself in order
to consume 3rd party Web services via RESTful APIs—as in the following schematic.

A key aim of this assignment is to gain hands-on experience with HTTP fundamentals. Do
not use high level frameworks (Django, Flask, Nodejs, etc) as they abstract the low level
HTTP functionality. You will get a chance to use these frameworks in the 2nd assignment.
Here you are being asked to implement your own micro-framework.

## Requirements (summarized from assignment pdf)

1. Use basic HTTP authentication to protect your site. Implement this in your Python server
so that without the correct login credentials, none of the resources will be accessible.

2. Respond to the following URI paths: '/', '/form', '/analysis', '/view/input', '/view/profile'.

3. Data from input and profile should be saved JSON format.

4. Fetch relevant movie data and pet images from a 3rd party site via RESTful API.

5. Use JavaScript functionality to fetch the psychological profile data together with any images.

6. Package the application as a Docker image


## How to use

- Run main.py
- The username and password are both 20019829. This is needed when logging onto the site.