install_dependencies:
	pip install -U -r requirements.txt

initialize:
	echo -e "{}\n" >> prefixes.json

run:
	python bot.py
