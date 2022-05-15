from models import User, db
from app import create_app

app = create_app()
app.app_context().push()

# attributes for User (not null)
#   username:       string      (pk)
#   password:       string
#   role:           string      default: "user"
#   dateCreated:    DateTime    default: func.now()

user = User(
    id=0,
    username="admin",
    password="....---.-...-",
    role="admin"
)

try:
    db.session.add(user)
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()
finally:
    db.session.close()