# Portfolio powered by Flask
This is a portfolio website built with Flask, using a simple JSON file as 
the project database.

# Run instructions
Either run the Flask Development server or use the Dockerfile.

## Development Server
```Bash
git clone https://github.com/Cinnamals/portfolio-flask.git && cd portfolio-flask
pip install flask flask-socketio
python3 myFlaskProject.py
```

## Docker
```Bash
git clone https://github.com/Cinnamals/portfolio-flask.git && cd portfolio-flask
docker build -t portfolio-flask .
docker run -p 3003:3003 portfolio-flask &
```
