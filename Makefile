.PHONY: api dev test spec-pdf

api:
	@PYTHONPATH=. uvicorn api.main:app --reload

dev: api

test:
	@PYTHONPATH=. python -m pytest -q

spec-pdf:
	@mkdir -p docs/spec dist
	@test -f docs/spec/book.md || echo "# Spec Book" > docs/spec/book.md
	@npx --yes md-to-pdf docs/spec/book.md
	@cp docs/spec/book.pdf dist/spec-book.pdf
	@ls -lh dist/spec-book.pdf
