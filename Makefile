.PHONY: spec test ajv all

spec:
	python3 scripts/render_spec.py

test:
	pytest -q

all: spec test
