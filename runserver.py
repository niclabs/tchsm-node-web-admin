import nodeadmin

nodeadmin.db.create_all()
app = nodeadmin.app

if __name__ == "__main__":
    app.run(debug=False)
