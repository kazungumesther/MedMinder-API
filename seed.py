import sys
import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base

# Direct explicit imports pointing to your models package folders
from app.models.medication import Medication
from app.models.reminder import Reminder
from app.models.adherence import AdherenceLog

def seed_database():
    print("🚀 Initializing mock healthcare database seed process...")
    
    # Force compile metadata paths
    _ = Medication
    _ = Reminder
    _ = AdherenceLog
    
    db: Session = SessionLocal()
    
    try:
        print("🧹 Cleaning existing data records...")
        db.query(AdherenceLog).delete()
        db.query(Reminder).delete()
        db.query(Medication).delete()
        
        # Clean profiles table cleanly using raw SQL
        db.execute(text("DELETE FROM profiles;"))
        db.commit()

        # 1. GENERATE THE UUID FIRST (Fixes the UnboundLocalError!)
        mock_user_uuid = uuid.uuid4()
        print(f"👤 Injecting parent user profile to satisfy foreign keys: {mock_user_uuid}")
        
        # 2. Insert into profiles using ONLY the ID column
                # 2. Insert into profiles using both the ID and a mock full name to pass your DB validation
               # 2. Insert into profiles using ID, full name, and email to satisfy all database rules
        db.execute(
            text("INSERT INTO profiles (id, full_name, email) VALUES (:user_id, :name, :email);"),
            {
                "user_id": mock_user_uuid, 
                "name": "John Doe (Test Account)",
                "email": "johndoe@example.com"
            }
        )
        db.commit()


      

        print("💊 Injecting sample medication tracking data...")
        amoxicillin = Medication(
            name="Amoxicillin (Antibiotic)",
            dosage="500mg - 1 capsule",
            stock_quantity=21,
            user_id=mock_user_uuid
        )
        lisinopril = Medication(
            name="Lisinopril (Blood Pressure)",
            dosage="10mg - Half tablet",
            stock_quantity=90,
            user_id=mock_user_uuid
        )
        vitamin_d = Medication(
            name="Vitamin D3",
            dosage="2000 IU",
            stock_quantity=5,
            user_id=mock_user_uuid
        )

        db.add_all([amoxicillin, lisinopril, vitamin_d])
        db.commit()
        
        print("⏰ Mapping notification schedules...")
        reminder_1 = Reminder(medication_id=amoxicillin.id, reminder_time="08:00", is_active=True)
        reminder_2 = Reminder(medication_id=amoxicillin.id, reminder_time="20:00", is_active=True)
        reminder_3 = Reminder(medication_id=lisinopril.id, reminder_time="06:30", is_active=True)
        reminder_4 = Reminder(medication_id=vitamin_d.id, reminder_time="12:00", is_active=True)

        db.add_all([reminder_1, reminder_2, reminder_3, reminder_4])
        db.commit()

        print("📊 Generating historical compliance logs...")
        log_1 = AdherenceLog(reminder_id=reminder_1.id, status="taken")
        log_2 = AdherenceLog(reminder_id=reminder_3.id, status="taken")
        log_3 = AdherenceLog(reminder_id=reminder_4.id, status="taken") # Changed to taken to clear constraint

        db.add_all([log_1, log_2, log_3])
        db.commit()

        print("✨ Database successfully populated with realistic data patterns!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Critical error occurred during seeding cycle: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
