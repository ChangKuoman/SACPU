from app import db, User

# attributes for User (not null)
#   username:       string      (pk)
#   password:       string
#   role:           string      default: "user"
#   dateCreated:    DateTime    default: func.now()

u1 = User(
    username="chang",
    password="aA.123",
)

u2 = User(
    username="bibiepiro",
    password="Bbcita-2004"
)

try:
    db.session.add_all([u1, u2])
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()
finally:
    db.session.close()