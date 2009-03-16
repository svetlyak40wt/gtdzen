check:
	PYTHONPATH=`pwd` tests/testsuite.py

dump:
	echo '.schema' | sqlite3 todo.sqlite
