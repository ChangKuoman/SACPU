from app import db, MotherBoard, User
from sqlalchemy import func

# default for User role="user", dateCreated=func.now()
u1 = User(
    username="HOLI123",
    password="aA.123",
)

try:
    db.session.add(u1)
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()
finally:
    db.session.close()

# default for Motherboard dateCreated=func.now(), dateModified=func.now()
m1 = MotherBoard(
    id=1,
    price=212.10,
    name="Motherboard AFOX IH61-MA2, Intel H61 LGA1155 DDR3, HDMI, VGA, RJ-45 LAN, 3 x HD Audio Jack",
    description="very interesting",
    dateCreated=func.now(),
    dateModified=func.now(),
)

m2 = MotherBoard(
    id=2,
    price=241.23,
    name="Motherboard AFOX IH81-MA, Intel H81 LGA1150, DDR3, VGA, HDMI, USB 3.0, LAN, Audio x3 ",
    description="very interesting",
    dateCreated=func.now(),
    dateModified=func.now(),
)

try:
    db.session.add_all([m1, m2])
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()
finally:
    db.session.close()