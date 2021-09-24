VenvActivate := "./env/Scripts/activate.bat"

.PHONY: requirements docs venv package

requirements:
	@pip install --upgrade pip
	@pip install virtualenv
	@pip install -r requirements.txt
	@pip install typer-cli

docs:
	@typer vsdownload/vsdownload.py utils docs --output CLI-API.md

venv:
	@python -m venv env
	@$(VenvActivate) && python -m pip install --upgrade pip
	@$(VenvActivate) && python -m pip install pyinstaller
	@$(VenvActivate) && python -m pip install -r requirements.txt

package: venv
	@$(VenvActivate) && pyinstaller main.py --name vsdownload --onefile
	@powershell -C "Remove-Item env -Recurse"
	@powershell -C "Remove-Item __pycache__ -Recurse"
	@powershell -C "Remove-Item build -Recurse"
	@powershell -C "Remove-Item vsdownload.spec"
