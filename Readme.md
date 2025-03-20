web framework:Python Fastapi
database : sqlite

using docker to run the app
docker compose up -d --build
Swagger docs:
http://localhost:8000/docs

local:
python -m venv envAPI
source envAPI/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
Swagger docs:
http://localhost:8001/docs









