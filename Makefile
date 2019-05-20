TEST = python -m pytest -vv tests/ $(arg) -p no:cacheprovider

.PHONY: clean
clean:
	-find service -type f -name "*.py[co]" -delete

.PHONY: test
test: clean
	$(TEST)
