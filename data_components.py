from models import Component, db
from app import create_app

app = create_app()
app.app_context().push()

# attributes for Component (not null)
#   id:             int         (pk), default: sequence
#   price:          float
#   name:           string      (unique)
#   description:    string
#   component_type:  string
#   dateCreated:    DateTime    default: func.now()
#   dateModified:   DateTime    default: func.now()

c1 = Component(
    id=501,
    price=169,
    name="T-FORCE VULCAN Z",
    component_type="RAM",
    description="Teamgroup, 8GB, DDR4, 3200 MHZ",
)

c2 = Component(
    id=502,
    price=189,
    name="VENGEANCE LPX",
    component_type="RAM",
    description="Corsair, 8GB, DDR4, 3000 MHZ, Sin RGB, SE007",
)

c3 = Component(
    id=503,
    price=96,
    name="Just another SSD",
    component_type="SSD",
    description="interesting description",
)

c4 = Component(
    id=504,
    price=88,
    name="Just an SSD",
    component_type="SSD",
    description="interesting description",
)

c5 = Component(
    id=505,
    price=500,
    name="Just an HDD",
    component_type="HDD",
    description="interesting description",
)

c6 = Component(
    id=506,
    price=510,
    name="Just another HDD",
    component_type="HDD",
    description="interesting description",
)

c7 = Component(
    id=507,
    price=800,
    name="Just an CPU",
    component_type="CPU",
    description="interesting description",
)

c8 = Component(
    id=508,
    price=46.48,
    name="Just another CPU",
    component_type="CPU",
    description="interesting description",
)

c9 = Component(
    id=509,
    price=808,
    name="Just an GPU",
    component_type="GPU",
    description="interesting description",
)

c10 = Component(
    id=510,
    price=462.48,
    name="Just another GPU",
    component_type="GPU",
    description="interesting description",
)

c11 = Component(
    id=511,
    price=872,
    name="Just an PSU",
    component_type="PSU",
    description="interesting description",
)

c12 = Component(
    id=512,
    price=75.4,
    name="Just another PSU",
    component_type="PSU",
    description="interesting description",
)

c13 = Component(
    id=513,
    price=75.7,
    name="Just an PC Cooling",
    component_type="PC Cooling",
    description="interesting description",
)

c14 = Component(
    id=514,
    price=7.48,
    name="Just another PC Cooling",
    component_type="PC Cooling",
    description="interesting description",
)

c15 = Component(
    id=515,
    price=778.4,
    name="A RAT",
    component_type="Peripheral",
    description="interesting description",
)

c16 = Component(
    id=516,
    price=42,
    name="HEADPHONES",
    component_type="Peripheral",
    description="interesting description",
)

c17 = Component(
    id=517,
    price=5.4,
    name="KEYBOARD",
    component_type="Peripheral",
    description="interesting description",
)

c18 = Component(
    id=518,
    price=48.86,
    name="MICROPHONE",
    component_type="Peripheral",
    description="interesting description",
)

try:
    db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18])
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()
finally:
    db.session.close()