
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3


setup:
	@mkdir resource/img/ logs/
	@cp resource/example_sources.json resource/sources.json
	sudo apt install ffmpeg 
	@python3 -m venv $(VENV) 
	@$(PIP) install -r requirements.txt 
	
	@printf "\n\nSetup Complete! \n"


run:
	@$(PYTHON) terminal_radio/main.py

