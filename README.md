
# Real-Time Chat Application (Django + Channels)

A production-ready real-time private chat application built using Django and Django Channels, enabling seamless WebSocket-based communication.

---

## Features

* User Authentication
* Private 1-to-1 Chat
* Real-Time Messaging (WebSockets)
* Typing Indicator
* Live Read Receipts
* Real-Time Unread Message Badge Updates
* Clean and Scalable Project Structure
* Static File Separation (CSS Organized Properly)

---

## Tech Stack

* Python 3.10+
* Django 5+
* Django Channels
* ASGI
* WebSockets
* HTML, CSS, JavaScript

---

## Installation Guide

### 1. Clone the Repository

    ```bash
    git clone https://github.com/DevAdithyan/realtime-chat-django.git
    cd chat_app
    ```

---

### 2. Create Virtual Environment

    ```bash
    python -m venv venv
    ```

Activate Virtual Environment

    Windows:

    ```bash
    venv\Scripts\activate
    ```

    Mac/Linux:

    ```bash
    source venv/bin/activate
    ```

---

### 3. Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```

---

### 4. Apply Database Migrations

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

---

### 5. Create Superuser

    ```bash
    python manage.py createsuperuser
    ```

---

### 6. Run Development Server

    ```bash
    python manage.py runserver
    ```

---

## Access the Application

Open your browser and go to:

    ```
    http://127.0.0.1:8000/
    ```

---

## Project Structure (Simplified)

```
chat_app/
│
├── chat_app/        # Main project settings
├── chat/            # Chat application
├── templates/
├── static/
├── manage.py
├── requirements.txt
└── README.md
```

## Author

Developed by Adithyan A


