# ----------------------------------
#          LIST TARGETS
# ----------------------------------
.PHONY: list
list:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* api/*.py

black:
	@black scripts/* api/*.py

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr package-*.dist-info
	@rm -fr package.egg-info

install:
	@pip install . -U

all: clean install test black check_code

# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

clean-notebooks:
	-@find . -name *.ipynb -exec jupyter nbconvert --clear-output --inplace {} \;

