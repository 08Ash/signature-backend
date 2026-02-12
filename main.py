from fastapi import FastAPI, UploadFile, File
from database import Base, engine, SessionLocal
from models import User, Document
from security import hash_pw, verify_pw, create_token
from pdf_service import sign_pdf
from audit import log_action
import shutil
import os

# Create database tables
Base.metadata.create_all(engine)

app = FastAPI()

UPLOAD_DIR = "uploads"
SIGNED_DIR = "signed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(SIGNED_DIR, exist_ok=True)


# ------------------------
# AUTH ROUTES
# ------------------------

@app.post("/register")
def register(email: str, password: str):
    db = SessionLocal()

    user = User(email=email, password=hash_pw(password))
    db.add(user)
    db.commit()

    log_action("User registered")

    db.close()

    return {"message": "User registered"}


@app.post("/login")
def login(email: str, password: str):
    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_pw(password, user.password):
        db.close()
        return {"error": "Invalid credentials"}

    token = create_token({"user_id": user.id})

    log_action("User logged in")

    db.close()

    return {"token": token}


# ------------------------
# DOCUMENT UPLOAD
# ------------------------

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    db = SessionLocal()
    db.add(Document(filename=file.filename))
    db.commit()
    db.close()

    log_action("PDF uploaded")

    return {"filename": file.filename}


# ------------------------
# PDF SIGNING
# ------------------------

@app.post("/sign/{filename}")
def sign_document(filename: str):
    input_pdf = os.path.join(UPLOAD_DIR, filename)
    signed_pdf = os.path.join(SIGNED_DIR, f"signed_{filename}")

    sign_pdf(input_pdf, signed_pdf)

    log_action("PDF signed")

    return {"signed_file": signed_pdf}


# ------------------------
# ROOT CHECK
# ------------------------

@app.get("/")
def home():
    return {"status": "Document Signature Backend Running"}
