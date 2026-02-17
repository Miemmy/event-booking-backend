# 🎟️ Event Booking API

A robust, high-performance REST API for managing events and ticket bookings. Built with **FastAPI** and **MongoDB**, featuring atomic transactions, JWT authentication, and automated seat management.

---

## 🚀 Live Demo & Documentation

**The easiest way to test this API is via the interactive Swagger documentation.**

* **📖 Live Swagger UI:** [https://event-booking-backend-1-7x1t.onrender.com/docs](https://event-booking-backend-1-7x1t.onrender.com/docs)
* **📖 Alternative (ReDoc):** [https://event-booking-backend-1-7x1t.onrender.com/redoc](https://event-booking-backend-1-7x1t.onrender.com/redoc)
* **🌍 Base URL:** `https://event-booking-backend-1-7x1t.onrender.com`

---

## ⚡ Features

### 👤 User Management
* **Secure Authentication:** JWT-based login and registration (OAuth2 Password Flow).
* **Role-Based Access:** Separation between basic `user` and `organizer` roles.
* **Profile Privacy:** Users can only view their own booking history.

### 📅 Event Management
* **Lifecycle Control:** Events start as `draft` (private) and can be published to go live.
* **Organizer Dashboard:** Organizers can view guest lists and manage their events.
* **Smart Filtering:** Search events by keyword, location, or date.
* **Safety Checks:** Automatic blocking of past dates.

### 🎫 Booking System (The Core)
* **Concurrency Safe:** Uses **MongoDB Atomic Updates (`$inc`)** to prevent double-booking (race conditions).
* **Soft Deletes:** Cancellations return seats to the pool but keep a historical record (`status="cancelled"`).
* **Validation:** Prevents duplicate bookings and enforces capacity limits.

---

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
* **Database:** [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
* **ODM:** [Beanie](https://beanie-odm.dev/) (Asynchronous MongoDB ODM)
* **Authentication:** PyJWT & Passlib (Bcrypt hashing)
* **Deployment:** Render

---

## 🔐 Authentication Flow

This API uses **Bearer Token Authentication**.

1.  **Register** a new user (`POST /auth/register`).
2.  **Login** with email/password to get an access token (`POST /auth/login`).
3.  **Authenticate Requests:** Include the token in the header of all protected requests.

**Header Format:**
```http
Authorization: Bearer <your_access_token>


## Local Setup Guide

### 1. Clone the Repository

First, clone the repository to your local machine and navigate into the project directory:

```bash
git clone https://github.com/YOUR_USERNAME/event-booking-backend.git
cd event-booking-backend
```

---

### 2. Create and Activate a Virtual Environment

It is recommended to use a virtual environment to manage project dependencies.

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

Install all required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```env
MONGO_URI=mongodb+srv://<user>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
SECRET_KEY=your_super_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Make sure to replace `<user>` and `<password>` with your actual MongoDB credentials. The `SECRET_KEY` should be a strong, unique string used for signing JWT tokens.

---

### 5. Run the Development Server

Start the FastAPI development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

Once the server starts successfully, the API will be available at:

```
http://127.0.0.1:8000
```

You can access the interactive API documentation at:

```
http://127.0.0.1:8000/docs
```

---
