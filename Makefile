init:
	pip install -r requirements.txt

test:
	nosetests --nocapture \
		  --with-coverage --cover-package currency \
		  --cover-html --cover-html-dir=htmlcov\
		  tests
