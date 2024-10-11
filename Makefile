
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3


setup:
	@mkdir resource/img/ logs/
	@cp resource/sources.example.json resource/sources.json
	sudo apt install ffmpeg 
	@python3 -m venv $(VENV) 
	@$(PIP) install -r requirements.txt 
	
	@printf "\n\nSetup Complete! \n"


run:
	@$(PYTHON) main.py play


update:
	@$(PYTHON) main.py update
	
