.PHONY: api dev test spec-pdf

api:
\tPYTHONPATH=. uvicorn api.main:app --reload

dev: api

test:
\tPYTHONPATH=. python -m pytest -q

spec-pdf:
\tmkdir -p dist
\tnpx --yes md-to-pdf docs/spec/book.md dist/spec-book.pdf
