# University-Management-System

A Python desktop application for managing a university or college system. The project includes admin/user management, course and department records, student tracking, and PDF export functionality.

## Overview

This project is built using Python and Tkinter and is designed for local desktop use in a college management workflow. It provides a simple interface for administrators to manage departments, student records, course details, and user roles.

## Features

- Admin portal with login support
- User management for Admin and Employee roles
- Department and course management
- Student record creation, updates, and search
- Department-wise record viewing
- PDF export of student records
- User profile images with face detection support

## Admin Portal

The admin portal is the central control section of the application.

### Default admin login

- Username: `admin`
- Password: `admin`

### Admin actions

- Add new users
- Update existing users
- Delete users
- Assign user type: Admin or Employee
- Search/filter records
- Manage department/course data
- View and print student reports

## Project Structure

```text
MyCollegeManager/
├── Coursepage.py
├── Recordpage2.py
├── Userpage.py
├── Capture_pic.py
├── printoutpage.py
├── face_recognition.py
├── pymysql.py
├── user_image/
├── face_requirements/
├── README.md
├── requirements.txt
└── .gitignore
```

## Tech Stack

- Python 3.9
- Tkinter
- MySQL
- Pillow
- tkcalendar
- face_recognition
- OpenCV / dlib

## Prerequisites

1. Install Python 3.9
2. Install Visual Studio C++ Build Tools if you want to build `dlib` and `face_recognition` locally
3. Install MySQL and create a database named `my_college_db`
4. Ensure the `user_image` folder exists

## Setup Instructions

### 1) Clone the repository

```bash
git clone https://github.com/Ayush-Gaautam/University-Management-System.git
cd University-Management-System
```

### 2) Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Create the database

Open MySQL and run:

```sql
CREATE DATABASE my_college_db;
```

Then create the necessary tables:

```sql
CREATE TABLE department (
    dname VARCHAR(255) PRIMARY KEY
);

CREATE TABLE course (
    dname VARCHAR(255),
    cname VARCHAR(255) PRIMARY KEY,
    fee VARCHAR(255),
    duration VARCHAR(255),
    units VARCHAR(255)
);

CREATE TABLE student (
    rollno VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    phone VARCHAR(255),
    gender VARCHAR(255),
    dob VARCHAR(255),
    address VARCHAR(255),
    department VARCHAR(255),
    course VARCHAR(255)
);

CREATE TABLE user (
    username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255),
    usertype VARCHAR(255),
    picture VARCHAR(255)
);
```

### 5) Run the application

From the project root, use:

```bash
python MyCollegeManager\Coursepage.py
python MyCollegeManager\Userpage.py
python MyCollegeManager\Recordpage2.py
```

You can also run these directly from your editor or IDE.

## Login Flow

1. Start the user management screen.
2. Enter the admin credentials:
   - Username: `admin`
   - Password: `admin`
3. Use the admin portal to manage the system.

## Notes

- The project currently uses a local MySQL connection on `localhost`.
- The default MySQL settings in the code are:
  - user: `root`
  - password: empty string
- Update these values if your database is configured differently.

## License

This project is intended for academic and educational use.
