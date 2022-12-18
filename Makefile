PYLINT_MODULES="./src/clabaireacht"
-include Makefiles/main.mk

.PHONY=run_prod: 
run_prod: ## Run web app in gunicorn- https, localhost, port 8443
	@echo Run web application in gunicorn
	cd ./src/ && gunicorn --bind 127.0.0.1:8443 -w 1 'clabaireacht:create_app()' --keyfile ../key.pem --certfile ../cert.pem

.PHONY=run_dev
run_dev: ## Run web application in flask- http,localhost, port 5000
	@echo Run web application in flask 
	cd ./src/ && flask --app clabaireacht --debug run