from app import app
import os

#app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
