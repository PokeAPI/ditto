.PHONY: clean data serve

data:
	python3 ditto.py capture

serve:
	python3 ditto.py transform --port 8080

clean:
	rm -r data
