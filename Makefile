init:
	pip install -r requirements.txt

init2:
	pip2 install -r requirements.txt

test:
	python3 /usr/bin/nosetests   \
	    --nocapture              \
	    --with-coverage          \
	    --cover-package scripts  \
	    --cover-package currency \
	    --cover-html             \
	    --cover-html-dir=htmlcov \
	    tests
	#
	python2 /usr/bin/nosetests   \
	    --nocapture              \
	    --with-coverage          \
	    --cover-package scripts  \
	    --cover-package currency \
	    --cover-html             \
	    --cover-html-dir=htmlcov \
	    tests
