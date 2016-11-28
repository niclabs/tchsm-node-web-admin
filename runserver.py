from nodeadmin import app, db 

db.create_all()
app.run(debug=False)