.PHONY: install run clean

install:
	./install.sh

run:
	./run.sh

clean:
	rm -rf .venv venv iphone-link.log .pane_webview_storage
