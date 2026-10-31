.PHONY: install run clean

install:
	./install.sh

run:
	./run.sh

clean:
	rm -rf .venv iphone-link.log
