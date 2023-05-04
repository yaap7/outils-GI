format:
	black .

dev_server: export FLASK_APP=app.py
dev_server: export FLASK_ENV=development
dev_server:
	flask run
