from app import app
import env

if __name__ == '__main__':
    app.run(port=env.PORT)
