PYTHON  ?= python3
VENV    := backend/.venv
CFLAGS  := -O2 -Wall -Wextra -fPIC
LIB     := backend/c/libed2.so
SRCS    := $(wildcard backend/c/*.c)

.PHONY: dev install lib back front test clean

# Sobe backend (:8000) e frontend (:5173) juntos
dev: install lib
	$(MAKE) -j2 back front

install: $(VENV)/bin/uvicorn frontend/node_modules

$(VENV)/bin/uvicorn: backend/requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -r backend/requirements.txt

frontend/node_modules: frontend/package.json
	cd frontend && npm install

lib: $(LIB)

$(LIB): $(SRCS) $(wildcard backend/c/*.h)
	gcc $(CFLAGS) -shared -o $@ $(SRCS)

back:
	cd backend && .venv/bin/uvicorn app.main:app --reload --port 8000

front:
	cd frontend && npm run dev

test: lib
	cd backend && .venv/bin/python -m unittest discover -s tests -t . -v

clean:
	rm -f $(LIB)
