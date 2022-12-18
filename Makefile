PYLINT_MODULES="./src/clabaireacht"
-include Makefiles/main.mk

.PHONY=run_prod:
run_prod:
	@echo Run web application in gunicorn
	cd ./src/ && gunicorn --bind 127.0.0.1:8443 -w 1 'clabaireacht:create_app()' --keyfile ../key.pem --certfile ../cert.pem

.PHONY=run_dev
run_dev:
	@echo Run web application in flask 
	cd ./src/ && flask --app clabaireacht --debug run