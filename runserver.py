import nodeadmin
from sqlalchemy.exc import SQLAlchemyError

nodeadmin.db.create_all()
app = nodeadmin.app

admin_user = nodeadmin.User(app.config['ADMIN_EMAIL'], app.config['ADMIN_PASSWORD'])
results = nodeadmin.db.session.query(nodeadmin.User).filter_by(email=admin_user.email).all()
if len(results) == 0:
    print("Couldn't find admin user. Creating one with credentials from config")
    try:
        nodeadmin.db.session.add(admin_user)
        nodeadmin.db.session.commit()
    except SQLAlchemyError as e:
        print("Failed to create admin user")
        print(e)

if __name__ == "__main__":
    app.run(debug=False)
