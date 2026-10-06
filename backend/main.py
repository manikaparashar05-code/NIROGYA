from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import bcrypt

from database import get_db_connection


app = FastAPI(title="NIROGYA API")


# =====================================================
# REQUEST MODELS
# =====================================================

class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str
    role: str = "patient"


class LoginRequest(BaseModel):
    email: str
    password: str


class PredictionHistoryRequest(BaseModel):
    user_id: int
    glucose: float
    blood_pressure: float
    bmi: float
    age: int
    pregnancies: int
    prediction: str
    risk_probability: float


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to NIROGYA 🧬",
        "status": "API is running",
        "database": "Connected"
    }


# =====================================================
# REGISTER
# =====================================================

@app.post("/register")
def register_user(user: RegisterRequest):

    connection = get_db_connection()

    if connection is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor()

    # Check if email already exists
    cursor.execute(
        "SELECT id FROM users WHERE email = %s",
        (user.email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        cursor.close()
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password
    password_hash = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # Insert user
    cursor.execute(
        """
        INSERT INTO users
        (full_name, email, password_hash, role)
        VALUES (%s, %s, %s, %s)
        """,
        (
            user.full_name,
            user.email,
            password_hash,
            user.role
        )
    )

    connection.commit()

    user_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return {
        "message": "Registration successful 🎉",
        "user_id": user_id,
        "name": user.full_name,
        "email": user.email,
        "role": user.role
    }


# =====================================================
# LOGIN
# =====================================================

@app.post("/login")
def login_user(user: LoginRequest):

    connection = get_db_connection()

    if connection is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email = %s",
        (user.email,)
    )

    db_user = cursor.fetchone()

    cursor.close()
    connection.close()

    if db_user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Check password
    password_match = bcrypt.checkpw(
        user.password.encode("utf-8"),
        db_user["password_hash"].encode("utf-8")
    )

    if not password_match:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful 🎉",
        "user_id": db_user["id"],
        "name": db_user["full_name"],
        "email": db_user["email"],
        "role": db_user["role"]
    }


# =====================================================
# SAVE PREDICTION HISTORY
# =====================================================

@app.post("/prediction-history")
def save_prediction_history(
    data: PredictionHistoryRequest
):

    connection = get_db_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO prediction_history
            (
                user_id,
                glucose,
                blood_pressure,
                bmi,
                age,
                pregnancies,
                prediction,
                risk_probability
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data.user_id,
                data.glucose,
                data.blood_pressure,
                data.bmi,
                data.age,
                data.pregnancies,
                data.prediction,
                data.risk_probability
            )
        )

        connection.commit()

        history_id = cursor.lastrowid

        return {
            "message": "Prediction history saved successfully",
            "history_id": history_id
        }

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Could not save prediction history: {str(e)}"
        )

    finally:

        cursor.close()
        connection.close()


# =====================================================
# GET PREDICTION HISTORY
# =====================================================

@app.get("/prediction-history/{user_id}")
def get_prediction_history(user_id: int):

    connection = get_db_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                id,
                glucose,
                blood_pressure,
                bmi,
                age,
                pregnancies,
                prediction,
                risk_probability,
                created_at
            FROM prediction_history
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        history = cursor.fetchall()

        return history

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not fetch prediction history: {str(e)}"
        )

    finally:

        cursor.close()
        connection.close()