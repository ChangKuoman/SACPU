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
    componentType="RAM",
    description="Teamgroup, 8GB, DDR4, 3200 MHZ",
)

c2 = Component(
    id=2,
    price=189,
    name="VENGEANCE LPX",
    componentType="RAM",
    description="Corsair, 8GB, DDR4, 3000 MHZ, Sin RGB, SE007",
)

c3 = Component(
    id=3,
    price=96,
    name="Just another SSD",
    componentType="SSD",
    description="interesting description",
)

c4 = Component(
    id=4,
    price=88,
    name="Just an SSD",
    componentType="SSD",
    description="interesting description",
)

c5 = Component(
    id=5,
    price=500,
    name="Just an HDD",
    componentType="HDD",
    description="interesting description",
)

c6 = Component(
    id=6,
    price=510,
    name="Just another HDD",
    componentType="HDD",
    description="interesting description",
)

c7 = Component(
    id=7,
    price=800,
    name="Just an CPU",
    componentType="CPU",
    description="interesting description",
)

c8 = Component(
    id=8,
    price=46.48,
    name="Just another CPU",
    componentType="CPU",
    description="interesting description",
)

c9 = Component(
    id=9,
    price=808,
    name="Just an GPU",
    componentType="GPU",
    description="interesting description",
)

c10 = Component(
    id=10,
    price=462.48,
    name="Just another GPU",
    componentType="GPU",
    description="interesting description",
)

c11 = Component(
    id=11,
    price=872,
    name="Just an PSU",
    componentType="PSU",
    description="interesting description",
)

c12 = Component(
    id=12,
    price=75.4,
    name="Just another PSU",
    componentType="PSU",
    description="interesting description",
)

c13 = Component(
    id=13,
    price=75.7,
    name="Just an PC Cooling",
    componentType="PC Cooling",
    description="interesting description",
)

c14 = Component(
    id=14,
    price=7.48,
    name="Just another PC Cooling",
    componentType="PC Cooling",
    description="interesting description",
)

c15 = Component(
    id=15,
    price=778.4,
    name="A RAT",
    componentType="Peripheral",
    description="interesting description",
)

c16 = Component(
    id=16,
    price=42,
    name="HEADPHONES",
    componentType="Peripheral",
    description="interesting description",
)

c17 = Component(
    id=17,
    price=5.4,
    name="KEYBOARD",
    componentType="Peripheral",
    description="interesting description",
)

c18 = Component(
    id=18,
    price=48.86,
    name="MICROPHONE",
    componentType="Peripheral",
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