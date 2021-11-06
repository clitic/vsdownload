VenvActivate := "./env/Scripts/activate.bat"
SitePackages := %LOCALAPPDATA%\Programs\Python\Python38\Lib\site-packages

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
	@pip install pip --upgrade
	@pip install virtualenv
	@pip install -r requirements.txt
	@pip install PyQt6

updates:
	@pyuic6 vsdownload/vsdownload.ui -x -o vsdownload/vsdownload_ui.py

docs:
	@pip install typer-cli --upgrade
	@typer vsdownload/vsdownload.py utils docs --output docs/CLI-API.md
	@pip install typer --upgrade
	@pip install click --upgrade

venv:
	@python -m venv env
	@$(VenvActivate) && python -m pip install --upgrade pip
	@$(VenvActivate) && python -m pip install pyinstaller
	@$(VenvActivate) && python -m pip install -r requirements.txt

package: venv
	@$(VenvActivate) && pyinstaller main.py \
	--name vsdownload --onefile --noconfirm \
	--add-data "$(SitePackages)\selenium;selenium" --add-data "$(SitePackages)\Crypto;Crypto"

	@powershell -C "Remove-Item vsdownload.spec"
	@powershell -C "Remove-Item env -Recurse"
	@powershell -C "Remove-Item __pycache__ -Recurse"
	@powershell -C "Remove-Item build -Recurse"

gui: venv
	@$(VenvActivate) && python -m pip install PyQt6

	@$(VenvActivate) && pyinstaller main.py \
	--name vsdownload --noconfirm \
	--add-data "$(SitePackages)\selenium;selenium" --add-data "$(SitePackages)\Crypto;Crypto"

	@powershell -C "Rename-Item -Path dist -NewName dist_cli"

	@$(VenvActivate) && pyinstaller main_gui_wrapper.py \
	--name vsdownload_gui --noconfirm --noconsole \
	--add-data "$(SitePackages)\selenium;selenium" --add-data "$(SitePackages)\Crypto;Crypto"

	@powershell -C "Copy-Item -Path dist_cli/vsdownload/* -Destination dist/vsdownload_gui -Recurse -Force"
	@powershell -C "Compress-Archive -Path dist/vsdownload_gui -DestinationPath dist/vsdownload_gui.zip"
	@powershell -C "Remove-Item env -Recurse"
	@powershell -C "Remove-Item __pycache__ -Recurse"
	@powershell -C "Remove-Item build -Recurse"
	@powershell -C "Remove-Item dist_cli -Recurse"
	@powershell -C "Remove-Item vsdownload.spec"
	@powershell -C "Remove-Item vsdownload_gui.spec"
