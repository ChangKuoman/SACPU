from models import Compatible, db
from app import create_app

app = create_app()
app.app_context().push()

# attributes for Compatible (not null)
#   id_motherboard: int         (fk -> motherboard.id)
#   id_component:   int         (fk -> component.id)
#   dateCreated:    DateTime    default: func.now()
#   dateModified:   DateTime    default: func.now()

c1 = Compatible(
    id_motherboard=501,
    id_component=501,
)

c2 = Compatible(
    id_motherboard=501,
    id_component=502,
)

c3 = Compatible(
    id_motherboard=501,
    id_component=503,
)

c4 = Compatible(
    id_motherboard=501,
    id_component=504,
)

c5 = Compatible(
    id_motherboard=501,
    id_component=505,
)

c6 = Compatible(
    id_motherboard=501,
    id_component=506,
)

c7 = Compatible(
    id_motherboard=501,
    id_component=507,
)

c8 = Compatible(
    id_motherboard=501,
    id_component=508,
)

c9 = Compatible(
    id_motherboard=501,
    id_component=509,
)

c10 = Compatible(
    id_motherboard=501,
    id_component=510,
)

c11 = Compatible(
    id_motherboard=501,
    id_component=511,
)

c12 = Compatible(
    id_motherboard=501,
    id_component=512,
)

c13 = Compatible(
    id_motherboard=501,
    id_component=513,
)

c14 = Compatible(
    id_motherboard=501,
    id_component=514,
)

c15 = Compatible(
    id_motherboard=501,
    id_component=515,
)

c16 = Compatible(
    id_motherboard=501,
    id_component=516,
)

c17 = Compatible(
    id_motherboard=501,
    id_component=517,
)

c18 = Compatible(
    id_motherboard=501,
    id_component=518,
)

c19 = Compatible(
    id_motherboard=502,
    id_component=501,
)

c20 = Compatible(
    id_motherboard=502,
    id_component=505,
)

try:
    db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20])
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()
finally:
    db.session.close()