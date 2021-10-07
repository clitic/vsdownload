VenvActivate := "./env/Scripts/activate.bat"

.PHONY: help requirements updates docs venv package gui

help:
	@echo make targets:
	@echo  requirements         install required dependencies
	@echo  updates              updates gui wrapper ui from vsdownload.ui
	@echo  docs                 generates CLI-API.md
	@echo  venv                 create virtual envoirnment
	@echo  package              create vsdownload.exe package
	@echo  gui                  create vsdownload_gui.exe and vsdownload.exe package
	@echo  help                 shows this help message

requirements:
	@pip install --upgrade pip
	@pip install virtualenv
	@pip install -r requirements.txt
	@pip install typer-cli

updates:
	@pyuic6 vsdownload/vsdownload.ui -x -o vsdownload/vsdownload_ui.py

docs:
	@typer vsdownload/vsdownload.py utils docs --output CLI-API.md

venv:
	@python -m venv env
	@$(VenvActivate) && python -m pip install --upgrade pip
	@$(VenvActivate) && python -m pip install pyinstaller
	@$(VenvActivate) && python -m pip install -r requirements.txt

package: venv
	@$(VenvActivate) && pyinstaller main.py --noconfirm --name vsdownload --onefile
	@powershell -C "Remove-Item vsdownload.spec"
	@powershell -C "Remove-Item env -Recurse"
	@powershell -C "Remove-Item __pycache__ -Recurse"
	@powershell -C "Remove-Item build -Recurse"

gui: venv
	@$(VenvActivate) && python -m pip install PyQt6
	@$(VenvActivate) && pyinstaller main.py --noconfirm --name vsdownload
	@powershell -C "Rename-Item -Path dist -NewName dist_cli"
	@$(VenvActivate) && pyinstaller main_gui_wrapper.py --noconfirm --name vsdownload_gui --noconsole
	@powershell -C "Copy-Item -Path dist_cli/vsdownload/* -Destination dist/vsdownload_gui -Recurse -Force"
	@powershell -C "Compress-Archive -Path dist/vsdownload_gui -DestinationPath dist/vsdownload_gui.zip"
	@powershell -C "Remove-Item env -Recurse"
	@powershell -C "Remove-Item __pycache__ -Recurse"
	@powershell -C "Remove-Item build -Recurse"
	@powershell -C "Remove-Item dist_cli -Recurse"
	@powershell -C "Remove-Item vsdownload.spec"
	@powershell -C "Remove-Item vsdownload_gui.spec"
