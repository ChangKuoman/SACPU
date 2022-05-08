from app import db, Component

# attributes for Component (not null)
#   id:             int         (pk), default: sequence
#   price:          float
#   name:           string      (unique)
#   description:    string
#   componentType:  string
#   dateCreated:    DateTime    default: func.now()
#   dateModified:   DateTime    default: func.now()

c1 = Component(
    id=1,
    price=169,
    name="T-FORCE VULCAN Z",
    componentType="RAM MEMORY",
    description="Teamgroup, 8GB, DDR4, 3200 MHZ",
)

c2 = Component(
    id=2,
    price=189,
    name="VENGEANCE LPX",
    componentType="RAM MEMORY",
    description="Corsair, 8GB, DDR4, 3000 MHZ, Sin RGB, SE007",
)

try:
    db.session.add_all([c1, c2])
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()
finally:
    db.session.close()