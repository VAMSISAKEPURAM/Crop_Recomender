# 🌾 Crop Recommendation System

A full-stack **Crop Recommendation Web Application** powered by **Machine Learning**, built with **Python (Flask)** on the backend and **HTML**, **CSS**, **JavaScript** on the frontend. The system predicts the most suitable crop to grow based on soil and environmental parameters using a trained **Random Forest Classifier**.

---

## 🗂️ Project Structure

```
crop-app/
│
├── app.py                      # Flask  application entry point & API routes
├── generate_model.py           # Script to train & save the ML model
├── requirements.txt            # Python dependencies
├── users.db                    # SQLite database (auto-created on first run)
│
├── model/
│   ├── crop_model.pkl          # Trained Random Forest model (serialized)
│   └── scaler.pkl              # Feature StandardScaler (serialized)
│
├── templates/
│   ├── base.html               # Base Jinja2 layout template
│   ├── index.html              # Main dashboard (prediction form)
│   ├── login.html              # User login page
│   ├── register.html           # User registration page
│   └── error.html              # Custom error page (404 / 500)
│
├── static/
│   ├── css/
│   │   └── style.css           # Global styling
│   └── js/
│       └── script.js           # Frontend logic & API interaction
│
└── README.md                   # Project documentation
```

---

## ⚙️ Prerequisites

Make sure the following are installed on your machine:

- **[Python](https://www.python.org/downloads/)** (v3.8 or higher recommended)
- **pip** (comes bundled with Python)

---

## 🚀 Setup & Run Instructions

### 1. Create & Activate a Virtual Environment *(Recommended)*

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs: `flask`, `numpy`, `pandas`, `scikit-learn`, `bcrypt`, `python-dotenv`, and `gunicorn`.

---

### 3. Generate the ML Model *(First-time only)*

> ⚠️ **Note:** This step is required only once before running the app for the first time. Skip this step if `model/crop_model.pkl` and `model/scaler.pkl` already exist.

```bash
python generate_model.py
```

This trains a **Random Forest Classifier** on a synthetic crop dataset and saves two files in the `model/` directory:
- `crop_model.pkl` — the trained classification model
- `scaler.pkl` — the `StandardScaler` for normalizing input features

---

### 4. Configure Environment Variables *(Optional)*

Create a `.env` file in the `crop-app/` root to set a custom secret key:

```env
SECRET_KEY=your-super-secret-key-here
```

> If `.env` is not provided, a default key is used automatically.

---

### 5. Start the Application

```bash
python app.py
```

The server will start on **http://localhost:5000**

---

### 6. Access the Application

Open your browser and go to:

```
http://localhost:5000
```

You will be redirected to the **Login** page. Register a new account to get started.

---

## 🔐 Authentication

This application uses **session-based authentication** with **bcrypt password hashing**.

| Action    | Details                                         |
|-----------|-------------------------------------------------|
| Register  | Create a new account at `/register`             |
| Login     | Log in with your credentials at `/login`        |
| Logout    | Ends your session and redirects to `/login`     |

> There is **no default admin account**. All users register and manage their own sessions.

---

## ✨ Features

### 🌱 Crop Prediction
- Input **7 soil & climate parameters** to get an instant crop recommendation
- Powered by a **Random Forest Classifier** with `StandardScaler` normalization
- Supports 7 crop classes: **Rice, Wheat, Maize, Lentil, Jute, Cotton, Sugarcane**
- Real-time prediction result displayed directly on the dashboard

### 🔐 User Authentication
- **Register** — Create a new account with a unique username & bcrypt-hashed password
- **Login / Logout** — Secure session-based access control
- All prediction routes are **protected** — only authenticated users can access the dashboard

### 🛡️ Robust Error Handling
- Custom **404** and **500** error pages
- Input validation on all 7 required fields before sending to the model
- Graceful model-not-found handling if `model/` files are missing

---

## 🤖 Machine Learning Model

| Property           | Value                          |
|--------------------|--------------------------------|
| Algorithm          | Random Forest Classifier       |
| Library            | scikit-learn                   |
| Input Features     | 7 (see below)                  |
| Output Classes     | 7 crops                        |
| Serialization      | Python `pickle`                |
| Preprocessing      | `StandardScaler` normalization |

### 📊 Input Features

| Feature       | Description                         | Unit       |
|---------------|-------------------------------------|------------|
| `N`           | Nitrogen content in soil            | mg/kg      |
| `P`           | Phosphorus content in soil          | mg/kg      |
| `K`           | Potassium content in soil           | mg/kg      |
| `temperature` | Average ambient temperature         | °C         |
| `humidity`    | Relative humidity                   | %          |
| `pH`          | Soil pH level                       | 0–14       |
| `rainfall`    | Average annual rainfall             | mm         |

### 🌾 Supported Crop Outputs

`Rice` · `Wheat` · `Maize` · `Lentil` · `Jute` · `Cotton` · `Sugarcane`

---

## 🗄️ Database Schema

The SQLite database (`users.db`) is auto-created on first launch and contains a single table:

### `users`

| Column     | Type    | Description                        |
|------------|---------|------------------------------------|
| `id`       | INTEGER | Auto-increment Primary Key         |
| `username` | TEXT    | Unique username (NOT NULL)         |
| `password` | TEXT    | bcrypt-hashed password (NOT NULL)  |

---

## 🌐 API Reference

All routes are served by `app.py` on **http://localhost:5000**.

| Method | Endpoint     | Auth Required | Description                         |
|--------|--------------|---------------|-------------------------------------|
| GET    | `/`          | ✅ Yes         | Render the main prediction dashboard |
| GET    | `/login`     | ❌ No          | Render the login page               |
| POST   | `/login`     | ❌ No          | Authenticate user and start session |
| GET    | `/register`  | ❌ No          | Render the registration page        |
| POST   | `/register`  | ❌ No          | Create a new user account           |
| GET    | `/logout`    | ✅ Yes         | Clear session and redirect to login |
| POST   | `/predict`   | ✅ Yes         | Accept soil data, return crop prediction (JSON) |

### `/predict` — Request & Response

**Request Body (JSON):**
```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.8,
  "humidity": 82.0,
  "pH": 6.5,
  "rainfall": 202.9
}
```

**Success Response:**
```json
{
  "success": true,
  "prediction": "Rice",
  "message": "Prediction successful."
}
```

**Error Response:**
```json
{
  "error": "Missing value for humidity."
}
```

---

## 🧩 Technical Architecture

```
Browser (Frontend)
       │
       │  HTML / CSS / JavaScript
       │  (Form inputs, validation, fetch API calls)
       ▼
Flask Server (app.py)
       │
       ├──► SQLite Database (users.db)
       │         └── User authentication
       │
       └──► ML Model (model/)
                 ├── scaler.pkl   → Feature normalization
                 └── crop_model.pkl → Random Forest prediction
```

- **Frontend** — Jinja2 HTML templates rendered by Flask, styled with custom CSS and powered by Vanilla JS for form handling and AJAX prediction requests.
- **Backend** — A Python Flask server manages routing, authentication, session management, and prediction logic.
- **ML Layer** — A pre-trained `scikit-learn` Random Forest model loaded at startup. The `StandardScaler` normalizes inputs before inference.
- **Database** — SQLite provides lightweight, file-based user account storage with no external database server required.

---

## 📦 Dependencies

| Package         | Purpose                                      |
|-----------------|----------------------------------------------|
| `flask`         | Web framework & routing                      |
| `numpy`         | Numerical array operations for ML inference  |
| `pandas`        | Data manipulation (model training)           |
| `scikit-learn`  | Random Forest model & StandardScaler         |
| `bcrypt`        | Secure password hashing                      |
| `python-dotenv` | Load environment variables from `.env`       |
| `gunicorn`      | Production WSGI server                       |

---

## 🚢 Production Deployment

To run in production using **Gunicorn**:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

> ⚠️ Make sure `DEBUG=False` and set a strong `SECRET_KEY` in your `.env` file before deploying.

---

## 📝 License

This project is built for educational purposes as part of an academic Machine Learning curriculum.

---

> Built with ❤️ for smart, data-driven agriculture
