DIR_PATH = $(shell pwd)
DIR_NAME = $(shell basename $$PWD)
DIR_TMP = /mnt/ramdisk/

help:
	@echo "clean - remove Python file artifacts"
	@echo "lint  - check style with flake8"
	@echo "test  - run unittests"
	@echo "setup - setup application"

setup:
	virtualenv -p python3 env
	. env/bin/activate && pip install -r requirements.txt

clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rfv
	find $(DIR_PATH)/logs/ | grep -E "(\.csv|\.json)" | xargs -d '\n' rm -rfv

test:
	python -m unittest discover tests -v

lint:
	flake8 --exclude .git,__pycache__,env,_ > _/lint.log

pack:
	rsync -arv --exclude-from '$(DIR_PATH)/_/rsync-exclude.txt' $(DIR_PATH) /mnt/ramdisk/
	cd $(DIR_TMP) && zip -r $(DIR_NAME).zip $(DIR_NAME)/*

pip_upgrade:
	pip install --upgrade pip
