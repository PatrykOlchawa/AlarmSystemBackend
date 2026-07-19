# Alarm System API

- FastAPI
- Python
- SQLite
- MQTT
- OpenCV
- React Native

#To run:
uvicorn app.main:app --reload
uvicorn app.main:app --host 0.0.0.0 --port 8000
#To generate docs:
http://localhost:8000/docs
http://localhost:8000/redoc

#Alembic
alembic revision --autogenerate -m "Note"
alembic upgrade head