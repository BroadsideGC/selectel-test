TEST = python -m pytest -vv tests/ -p no:cacheprovider

.PHONY: clean
clean:
	-find service -type f -name "*.py[co]" -delete

.PHONY: test
test: clean
	$(TEST)
