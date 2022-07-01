from modules import app
import os

app.secret_key = os.urandom(12)
app.run(debug=True, host='0.0.0.0')