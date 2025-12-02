# Healthcare-Emergency-SOS-System-Django
Healthcare Emergency SOS System  A full-stack Healthcare Emergency SOS Web Application built using Django REST Framework and modern front-end technologies that enables real-time emergency alerts by instantly sharing patient location and medical profile with nearby hospitals for faster response and lifesaving action.

🚑 Healthcare Emergency SOS App

A full-stack emergency response system that enables patients to send instant SOS alerts, along with their live location and health profile, directly to the hospital dashboard for rapid medical assistance.

🔍 Project Overview

The Healthcare Emergency SOS App is designed to reduce emergency response delays by connecting patients and hospitals in real time.
It provides a secure, fast, and automated way for users to request medical help during critical situations.

This system integrates:

Django REST API for backend processing

Responsive frontend using HTML, CSS, and JavaScript

Real-time alert delivery to hospital dashboards

Secure patient data management

✨ Key Features
🆘 Instant Emergency Alerts

One-tap SOS trigger

Sends patient details + live location to hospital dashboard

🏥 Hospital Dashboard

Displays incoming emergency requests

Real-time data updates

Patient history view (if stored)

🔐 Secure Backend

Django REST API ensures safe data handling

Token-based authentication (if implemented)

📍 Location Integration

Captures geolocation from the client device

Sends coordinates to the backend for emergency routing

📱 Responsive UI

Mobile-friendly interface

Clean and minimal design for quick access in emergencies

🛠️ Tech Stack

Frontend: HTML5, CSS3, JavaScript
Backend: Django, Django REST Framework
Database: MySQL / SQLite
Tools: VS Code, Postman, GitHub

📦 Features Implemented

User emergency profile creation

SOS trigger endpoint

Emergency notification module

Hospital admin dashboard pages

Live location integration

REST API for data transmission

Data validation & error handling

📚 Folder Structure (Example)
/healthcare-sos-app
│── backend/
│   ├── manage.py
│   ├── sos_api/
│   ├── hospital_dashboard/
│   └── ...
│── frontend/
│   ├── index.html
│   ├── sos.js
│   ├── styles.css
│── README.md
└── ...

🚀 How to Run
1️⃣ Clone the repository
git clone https://github.com/your-username/healthcare-sos-app.git

2️⃣ Set up backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

3️⃣ Run frontend

Open index.html in a browser.

📌 Future Enhancements

Real-time alerts using WebSockets

Hospital assignment based on distance

Patient mobile app version

AI-based priority prediction

Integration with maps for navigation
