from app import db, Compatible

# attributes for Compatible (not null)
#   id_motherboard: int         (fk -> motherboard.id)
#   id_component:   int         (fk -> component.id)
#   dateCreated:    DateTime    default: func.now()
#   dateModified:   DateTime    default: func.now()

c1 = Compatible(
    id_motherboard=1,
    id_component=2,
)

c2 = Compatible(
    id_motherboard=1,
    id_component=1,
)

c3 = Compatible(
    id_motherboard=2,
    id_component=1,
)

try:
    db.session.add_all([c1, c2, c3])
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()
finally:
    db.session.close()