install_dependencies:
	pip install -U -r requirements.txt

initialize:
	echo "{}\n" >> prefixes.json

run:
	python bot.py
