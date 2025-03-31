To do:

Will
- Implement and test visible failure reasoning in the result

Jamie, Gyanu & Sulav
- Expand unit tests to 100% code coverage

All (once coverage is to 100%)
- Edit code as needed until unit tests pass

Ahriel
- Choose a packaging library (such as pickle?) and prepare project for packing into an executable (to be done on completion)


# Documentation

## General

Terminal command to run the project from project root: PYTHONPATH=$PYTHONPATH:. python src/gui/gui_5_0.py

## Pytest

https://docs.pytest.org/en/stable/contents.html

Pytest terminal command (run from project root): 
 PYTHONPATH=$PYTHONPATH:. pytest -vvv --tb=long -rA \
       --cov=src \
       --cov-report=html:docs/pytest/coverage_reports/ \
       --html=docs/pytest/test_reports/report.html \
       --self-contained-html
