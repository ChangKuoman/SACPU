from app import db, Compatible

# attributes for Compatible (not null)
#   id_motherboard: int         (fk -> motherboard.id)
#   id_component:   int         (fk -> component.id)
#   dateCreated:    DateTime    default: func.now()
#   dateModified:   DateTime    default: func.now()

c1 = Compatible(
    id_motherboard=1,
    id_component=1,
)

c2 = Compatible(
    id_motherboard=1,
    id_component=2,
)

c3 = Compatible(
    id_motherboard=1,
    id_component=3,
)

c4 = Compatible(
    id_motherboard=1,
    id_component=4,
)

c5 = Compatible(
    id_motherboard=1,
    id_component=5,
)

c6 = Compatible(
    id_motherboard=1,
    id_component=6,
)

c7 = Compatible(
    id_motherboard=1,
    id_component=7,
)

c8 = Compatible(
    id_motherboard=1,
    id_component=8,
)

c9 = Compatible(
    id_motherboard=1,
    id_component=9,
)

c10 = Compatible(
    id_motherboard=1,
    id_component=10,
)

c11 = Compatible(
    id_motherboard=1,
    id_component=11,
)

c12 = Compatible(
    id_motherboard=1,
    id_component=12,
)

c13 = Compatible(
    id_motherboard=1,
    id_component=13,
)

c14 = Compatible(
    id_motherboard=1,
    id_component=14,
)

c15 = Compatible(
    id_motherboard=1,
    id_component=15,
)

c16 = Compatible(
    id_motherboard=1,
    id_component=16,
)

c17 = Compatible(
    id_motherboard=1,
    id_component=17,
)

c18 = Compatible(
    id_motherboard=1,
    id_component=18,
)

c19 = Compatible(
    id_motherboard=2,
    id_component=1,
)

c20 = Compatible(
    id_motherboard=2,
    id_component=5,
)

try:
    db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20])
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()
finally:
    db.session.close()