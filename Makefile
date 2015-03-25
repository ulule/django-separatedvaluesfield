pep8:
	flake8 separatedvaluesfield --ignore=E501,E127,E128,E124

test:
	coverage run --branch --source=separatedvaluesfield manage.py test separatedvaluesfield
	coverage report --omit=separatedvaluesfield/test*

release:
	python setup.py sdist register upload -s

.venv:
	virtualenv -p python2.7 `pwd`/.venv
	. .venv/bin/activate && pip install -r requirements.dev.pip

dev: .venv
	. .venv/bin/activate
