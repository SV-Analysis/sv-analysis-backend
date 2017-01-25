from app import app

# The port number should be the same as the front end
try:
    app.run(use_reloader=False, debug=True, port=9930)
except:
    print("Some thing wrong!")
