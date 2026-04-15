# 🗂️ Task Manager (Django + DRF + Vanilla JS)

A full-stack task management application with Kanban board
functionality, built with Django REST Framework (backend) and Vanilla
JavaScript (frontend).

------------------------------------------------------------------------

## 🚀 Features

-   🔐 Authentication (Register / Login / Logout)
-   📁 Project management (CRUD)
-   ✅ Task management (CRUD)
-   📌 Assign users to tasks
-   📊 Kanban board (Backlog / In Progress / Done)
-   🖱️ Drag & Drop task movement
-   ✏️ Task detail modal (edit & delete)
-   👥 Project members management

------------------------------------------------------------------------

## 🏗️ Tech Stack

**Backend** - Django - Django REST Framework - Token Authentication

**Frontend** - HTML, CSS - Vanilla JavaScript (ES Modules) - Fetch API

------------------------------------------------------------------------

## 📁 Project Structure

task-manager/ 
│ ├── backend/ 
│ ├── manage.py 
│ ├── requirements.txt │
├── config/ 
│ └── apps/ 
│ ├── accounts/ 
│ ├── projects/ 
│ └── tasks/ │
├── frontend/ 
│ ├── templates/ 
│ ├── static/ │ 
│ ├── css/ │ 
│ └── js/ │
└── README.md

------------------------------------------------------------------------

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

git clone https://github.com/crossgear/task-manager-system 
cd task-manager

------------------------------------------------------------------------

### 2️⃣ Backend setup

cd backend python -m venv venv 
source venv/bin/activate 

\# Linux/Mac
venv`\Scripts`{=tex}`\activate     `{=tex}

\# Windows
pip install -r requirements.txt

------------------------------------------------------------------------

### 3️⃣ Run migrations

python manage.py migrate

------------------------------------------------------------------------

### 4️⃣ Create superuser (optional)

python manage.py createsuperuser

------------------------------------------------------------------------

### 5️⃣ Run server

python manage.py runserver

------------------------------------------------------------------------

## 🌐 Usage

-   Open: http://127.0.0.1:8000/
-   Register a new user
-   Login
-   Create projects
-   Add tasks
-   Drag & drop tasks across columns
-   Assign users and edit tasks

------------------------------------------------------------------------

## 🔌 API Endpoints

### Auth

-   POST /api/v1/auth/register/
-   POST /api/v1/auth/login/

### Projects

-   GET /api/v1/projects/
-   POST /api/v1/projects/
-   GET /api/v1/projects/{id}/
-   DELETE /api/v1/projects/{id}/

### Tasks

-   GET /api/v1/projects/{id}/tasks/
-   POST /api/v1/projects/{id}/tasks/
-   PATCH /api/v1/tasks/{id}/
-   DELETE /api/v1/tasks/{id}/

------------------------------------------------------------------------

## 👤 Author

Victor Giménez

------------------------------------------------------------------------

## 📄 License

Educational use only.
