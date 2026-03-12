/*
 * ============================================================
 *  Student Management System
 *  Author  : Hala Anqawi
 *  Language: C++
 *  Topics  : Arrays, loops, functions, structs, input/output
 * ============================================================
 *
 *  Features:
 *    1. Add a new student
 *    2. Display all students
 *    3. Search by student ID
 *    4. Search by name
 *    5. Edit student record
 *    6. Delete a student
 *    7. Show class statistics (average GPA, highest, lowest)
 *    8. Exit
 */

#include <iostream>
#include <string>
#include <iomanip>
#include <limits>
#include <algorithm>

using namespace std;

// ── Constants ────────────────────────────────────────────────
const int MAX_STUDENTS = 100;

// ── Data structure ───────────────────────────────────────────
struct Student {
    int    id;
    string name;
    int    age;
    string major;
    double gpa;
    bool   active;   // soft-delete flag
};

// ── Global storage ───────────────────────────────────────────
Student students[MAX_STUDENTS];
int     studentCount = 0;
int     nextId       = 1001;

// ── Utility ──────────────────────────────────────────────────
void clearInput() {
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

void printLine(char ch = '-', int len = 56) {
    cout << string(len, ch) << "\n";
}

void printHeader(const string& title) {
    cout << "\n";
    printLine('=');
    cout << "  " << title << "\n";
    printLine('=');
}

void printStudentRow(const Student& s) {
    cout << "  " << left
         << setw(6)  << s.id
         << setw(22) << s.name
         << setw(5)  << s.age
         << setw(16) << s.major
         << fixed << setprecision(2) << s.gpa
         << "\n";
}

void printTableHeader() {
    printLine();
    cout << "  " << left
         << setw(6)  << "ID"
         << setw(22) << "Name"
         << setw(5)  << "Age"
         << setw(16) << "Major"
         << "GPA\n";
    printLine();
}

// ── Find index by ID (returns -1 if not found) ───────────────
int findById(int id) {
    for (int i = 0; i < studentCount; i++) {
        if (students[i].active && students[i].id == id)
            return i;
    }
    return -1;
}

// ── Feature 1: Add student ───────────────────────────────────
void addStudent() {
    if (studentCount >= MAX_STUDENTS) {
        cout << "  [!] Maximum capacity reached (" << MAX_STUDENTS << " students).\n";
        return;
    }

    printHeader("Add New Student");

    Student s;
    s.id     = nextId++;
    s.active = true;

    clearInput();

    cout << "  Full name   : ";
    getline(cin, s.name);

    cout << "  Age         : ";
    while (!(cin >> s.age) || s.age < 15 || s.age > 60) {
        cout << "  [!] Enter a valid age (15–60): ";
        cin.clear(); clearInput();
    }
    clearInput();

    cout << "  Major       : ";
    getline(cin, s.major);

    cout << "  GPA (0–4.0) : ";
    while (!(cin >> s.gpa) || s.gpa < 0.0 || s.gpa > 4.0) {
        cout << "  [!] Enter a valid GPA (0.0–4.0): ";
        cin.clear(); clearInput();
    }

    students[studentCount++] = s;

    cout << "\n  Student added successfully.\n";
    cout << "  Assigned ID : " << s.id << "\n";
}

// ── Feature 2: Display all ───────────────────────────────────
void displayAll() {
    printHeader("All Students");

    int count = 0;
    for (int i = 0; i < studentCount; i++)
        if (students[i].active) count++;

    if (count == 0) {
        cout << "  No students in the system yet.\n";
        return;
    }

    printTableHeader();
    for (int i = 0; i < studentCount; i++) {
        if (students[i].active)
            printStudentRow(students[i]);
    }
    printLine();
    cout << "  Total: " << count << " student(s)\n";
}

// ── Feature 3: Search by ID ──────────────────────────────────
void searchById() {
    printHeader("Search by Student ID");
    int id;
    cout << "  Enter student ID: ";
    cin  >> id;

    int idx = findById(id);
    if (idx == -1) {
        cout << "  [!] No student found with ID " << id << ".\n";
        return;
    }

    printTableHeader();
    printStudentRow(students[idx]);
    printLine();
}

// ── Feature 4: Search by name ────────────────────────────────
void searchByName() {
    printHeader("Search by Name");
    clearInput();
    string query;
    cout << "  Enter name (or part of name): ";
    getline(cin, query);

    // Case-insensitive comparison
    string queryLower = query;
    transform(queryLower.begin(), queryLower.end(), queryLower.begin(), ::tolower);

    bool found = false;
    printTableHeader();
    for (int i = 0; i < studentCount; i++) {
        if (!students[i].active) continue;
        string nameLower = students[i].name;
        transform(nameLower.begin(), nameLower.end(), nameLower.begin(), ::tolower);
        if (nameLower.find(queryLower) != string::npos) {
            printStudentRow(students[i]);
            found = true;
        }
    }
    printLine();
    if (!found)
        cout << "  [!] No matching students found for \"" << query << "\".\n";
}

// ── Feature 5: Edit student ──────────────────────────────────
void editStudent() {
    printHeader("Edit Student Record");
    int id;
    cout << "  Enter student ID to edit: ";
    cin  >> id;

    int idx = findById(id);
    if (idx == -1) {
        cout << "  [!] Student not found.\n";
        return;
    }

    Student& s = students[idx];
    cout << "\n  Current record:\n";
    printTableHeader();
    printStudentRow(s);
    printLine();

    clearInput();
    cout << "\n  Leave blank to keep the current value.\n\n";

    cout << "  New name [" << s.name << "]: ";
    string input;
    getline(cin, input);
    if (!input.empty()) s.name = input;

    cout << "  New age  [" << s.age << "]: ";
    getline(cin, input);
    if (!input.empty()) {
        try { int a = stoi(input); if (a >= 15 && a <= 60) s.age = a; }
        catch (...) {}
    }

    cout << "  New major [" << s.major << "]: ";
    getline(cin, input);
    if (!input.empty()) s.major = input;

    cout << "  New GPA  [" << fixed << setprecision(2) << s.gpa << "]: ";
    getline(cin, input);
    if (!input.empty()) {
        try { double g = stod(input); if (g >= 0 && g <= 4.0) s.gpa = g; }
        catch (...) {}
    }

    cout << "\n  Record updated successfully.\n";
}

// ── Feature 6: Delete student ────────────────────────────────
void deleteStudent() {
    printHeader("Delete Student");
    int id;
    cout << "  Enter student ID to delete: ";
    cin  >> id;

    int idx = findById(id);
    if (idx == -1) {
        cout << "  [!] Student not found.\n";
        return;
    }

    cout << "\n  Student to delete: " << students[idx].name << " (ID " << id << ")\n";
    cout << "  Confirm? (y/n): ";
    char confirm;
    cin  >> confirm;

    if (confirm == 'y' || confirm == 'Y') {
        students[idx].active = false;
        cout << "  Student removed.\n";
    } else {
        cout << "  Cancelled.\n";
    }
}

// ── Feature 7: Statistics ────────────────────────────────────
void showStatistics() {
    printHeader("Class Statistics");

    int    count    = 0;
    double total    = 0.0;
    double highest  = -1.0;
    double lowest   = 5.0;
    string topName, lowName;

    for (int i = 0; i < studentCount; i++) {
        if (!students[i].active) continue;
        count++;
        total += students[i].gpa;
        if (students[i].gpa > highest) { highest = students[i].gpa; topName = students[i].name; }
        if (students[i].gpa < lowest)  { lowest  = students[i].gpa; lowName = students[i].name; }
    }

    if (count == 0) {
        cout << "  No students to analyse.\n";
        return;
    }

    double avg = total / count;

    // GPA distribution
    int excellent = 0, good = 0, average = 0, poor = 0;
    for (int i = 0; i < studentCount; i++) {
        if (!students[i].active) continue;
        if      (students[i].gpa >= 3.7) excellent++;
        else if (students[i].gpa >= 3.0) good++;
        else if (students[i].gpa >= 2.0) average++;
        else                              poor++;
    }

    cout << fixed << setprecision(2);
    cout << "  Total students  : " << count << "\n";
    printLine();
    cout << "  Average GPA     : " << avg     << "\n";
    cout << "  Highest GPA     : " << highest << "  (" << topName << ")\n";
    cout << "  Lowest GPA      : " << lowest  << "  (" << lowName  << ")\n";
    printLine();
    cout << "  GPA Distribution:\n";
    cout << "    3.7 – 4.0  (Excellent) : " << excellent << " student(s)\n";
    cout << "    3.0 – 3.69 (Good)      : " << good      << " student(s)\n";
    cout << "    2.0 – 2.99 (Average)   : " << average   << " student(s)\n";
    cout << "    0.0 – 1.99 (Poor)      : " << poor      << " student(s)\n";
    printLine();
}

// ── Seed with demo data ──────────────────────────────────────
void seedDemoData() {
    string names[]  = {"Hala Anqawi","Sara Khalil","Yusuf Nasser","Layla Hassan","Omar Barakat"};
    int    ages[]   = {20, 22, 21, 23, 20};
    string majors[] = {"Artificial Intelligence","Computer Science",
                       "Data Science","Software Engineering","Artificial Intelligence"};
    double gpas[]   = {3.85, 3.40, 3.10, 3.70, 2.95};

    for (int i = 0; i < 5; i++) {
        Student s;
        s.id     = nextId++;
        s.name   = names[i];
        s.age    = ages[i];
        s.major  = majors[i];
        s.gpa    = gpas[i];
        s.active = true;
        students[studentCount++] = s;
    }
}

// ── Main menu ────────────────────────────────────────────────
int main() {
    seedDemoData();

    cout << "\n";
    printLine('=');
    cout << "    Student Management System\n";
    cout << "    Author: Hala Anqawi\n";
    printLine('=');
    cout << "  Demo data loaded: 5 students.\n";

    int choice = 0;
    do {
        cout << "\n";
        printLine();
        cout << "  MENU\n";
        printLine();
        cout << "  1. Add student\n";
        cout << "  2. Display all students\n";
        cout << "  3. Search by ID\n";
        cout << "  4. Search by name\n";
        cout << "  5. Edit student\n";
        cout << "  6. Delete student\n";
        cout << "  7. Class statistics\n";
        cout << "  0. Exit\n";
        printLine();
        cout << "  Choice: ";
        cin  >> choice;

        switch (choice) {
            case 1: addStudent();    break;
            case 2: displayAll();    break;
            case 3: searchById();    break;
            case 4: searchByName();  break;
            case 5: editStudent();   break;
            case 6: deleteStudent(); break;
            case 7: showStatistics();break;
            case 0: cout << "\n  Goodbye.\n\n"; break;
            default: cout << "  [!] Invalid option.\n"; break;
        }
    } while (choice != 0);

    return 0;
}
