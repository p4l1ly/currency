init:
	pip install -r requirements.txt

test:
	nosetests --nocapture --with-coverage --cover-package currency tests
