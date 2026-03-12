# Project 3 — Student Management System (C++)

A console-based student database system written in C++.

## Features
- Add new students with full validation
- Display all students in a formatted table
- Search by student ID
- Search by name (partial, case-insensitive)
- Edit any field of an existing record
- Delete a student (soft delete)
- Class statistics — average GPA, highest, lowest, grade distribution

## C++ concepts used
`structs` · arrays · loops · functions · string manipulation · input validation · `iomanip` formatting

## How to compile and run
```bash
g++ -std=c++17 -o student_system student_system.cpp
./student_system
```
Requires: any C++17-compatible compiler (g++, clang++, MSVC)

## Demo data
5 students are pre-loaded when the program starts so you can test all features immediately.

## Sample output
```
========================================================
  All Students
========================================================
--------------------------------------------------------
  ID    Name                  Age  Major           GPA
--------------------------------------------------------
  1001  Hala Anqawi           20   Artificial Intelligence  3.85
  1002  Sara Khalil           22   Computer Science         3.40
  ...
```
