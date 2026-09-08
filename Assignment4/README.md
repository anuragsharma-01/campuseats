# CampusEats — Assignment 4

Selected service: Orders Service.

Contents:
openapi.yaml
app.py
models.py
store.py
errors.py
tests/test_app.py
NOTES.md
curl-transcript.txt
VALIDATION_OUTPUT.txt
requirements.txt

Run:
pip install -r requirements.txt
export PAYMENT_SERVICE_URL=http://localhost:6000
python app.py

Test:
pytest -q
