# Alarm System API

- FastAPI
- Python
- SQLite
- MQTT
- OpenCV
- React Native

#To run:
#sudo docker compose up --build
#sudo docker compose down

#To generate docs:
http://localhost:8000/docs
http://localhost:8000/redoc

#Postgresql
sudo docker compose exec postgres psql -U alarm -d alarm_db

#Alembic
sudo docker compose exec backend alembic revision --autogenerate -m "Note"
sudo docker compose exec backend alembic upgrade head