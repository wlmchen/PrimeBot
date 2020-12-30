install_dependencies:
	pip install -U -r requirements.txt

initialize:
	echo "{}" >> prefixes.json

run:
	python bot.py
