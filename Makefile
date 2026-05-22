# ANSI color codes
COLOR_RESET=\033[0m
COLOR_BOLD=\033[1m
COLOR_GREEN=\033[32m
COLOR_YELLOW=\033[33m

# Detect the available Python interpreter:
# - Linux/macOS usually expose `python3` (and may not have `python`)
# - Windows usually exposes `python` (from python.org or the Store launcher)
PYTHON ?= $(shell command -v python3 2>/dev/null || command -v python 2>/dev/null)

help:
	@echo ""
	@echo "  $(COLOR_YELLOW)Available targets:$(COLOR_RESET)"
	@echo ""
	@echo "  $(COLOR_GREEN)upgrade-pip$(COLOR_RESET)		- Upgrade Pip Version"
	@echo "  $(COLOR_GREEN)install$(COLOR_RESET)		- Install Libraries / Dependencies"
	@echo "  $(COLOR_GREEN)freeze$(COLOR_RESET)		- Freeze Libraries / Dependencies"
	@echo "  $(COLOR_GREEN)database$(COLOR_RESET)		- Start PostgreSQL Database"
	@echo "  $(COLOR_GREEN)migrations$(COLOR_RESET)		- Run Database Migrations"
	@echo "  $(COLOR_GREEN)migrate$(COLOR_RESET)		- Apply Database Migrations"
	@echo "  $(COLOR_GREEN)superuser$(COLOR_RESET)		- Create Django superuser"
	@echo "  $(COLOR_GREEN)run$(COLOR_RESET)			- Run Django App"
	@echo "  $(COLOR_GREEN)test$(COLOR_RESET)			- Run the test suite"
	@echo ""
	@echo "  $(COLOR_YELLOW)Detected Python:$(COLOR_RESET) $(PYTHON)"
	@echo "  $(COLOR_YELLOW)Note:$(COLOR_RESET) Use 'make <target>' to execute a specific target."
	@echo ""

upgrade-pip:
	$(PYTHON) -m pip install --upgrade pip

freeze:
	$(PYTHON) -m pip freeze > requirements.txt

install:
	$(PYTHON) -m pip install -r requirements.txt

database:
	docker compose up -d

migrations:
	$(PYTHON) manage.py makemigrations

migrate:
	$(PYTHON) manage.py migrate

superuser:
	$(PYTHON) manage.py createsuperuser

run:
	$(PYTHON) manage.py runserver

test:
	$(PYTHON) manage.py test
