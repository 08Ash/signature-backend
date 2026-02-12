from database import SessionLocal
from models import Audit

def log_action(action: str):
    db = SessionLocal()

    audit = Audit(action=action)
    db.add(audit)
    db.commit()

    db.close()
