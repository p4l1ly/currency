init:
	pip install -r requirements.txt

test:
	nosetests --nocapture tests
