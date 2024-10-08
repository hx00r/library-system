
# Library System back-end

A RESTful API Library system that uses these stored procedures for
database operations.

## Overview
![App Screenshot](/overview.png)

Users can:
- Create a book
- List all books
- Retrieve a specific book by its `ID`
- Retrieve a specific book by its `title`
- Update a book
- Delete a book

## Entity Relation Diagram
![App Screenshot](/EER-Diagram_SS.png)

## Setup Steps
To setup this project run:

1- Clone the repo first:
```bash
  git clone https://github.com/hx00r/library-system
```
2- Install all python dependencies
```bash
  pip install requirements.txt
```
3- Start the server
```bash
  python manage.py runserver
```
## How to use
To use this project head to `/api/` and you will see the API documentation and try to send a request.
