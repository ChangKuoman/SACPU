from app import db, MotherBoard

# attributes for Motherboard (not null)
#   id:             int         (pk), default: sequence
#   price:          float
#   name:           string      (unique)
#   description:    string
#   dateCreated:    DateTime    default: func.now()
#   dateModified:   DateTime    default: func.now()

m1 = MotherBoard(
    id=1,
    price=212.10,
    name="AFOX IH61-MA2",
    description="very interesting",
)

m2 = MotherBoard(
    id=2,
    price=241.23,
    name="AFOX IH81-MA",
    description="very interesting",
)

try:
    db.session.add_all([m1, m2])
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()
finally:
    db.session.close()