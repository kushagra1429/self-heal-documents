from self_healing_docs.parsers.python_parser import classify

def test_default_argument_change_is_signature_change():
    old = 'def create_user(email, role="admin"): return email'
    new = 'def create_user(email, role="viewer"): return email'
    assert classify(old, new)[0][1] == "signature_changed"

def test_body_change_is_not_signature_change():
    old = "def total(x): return x + 1"
    new = "def total(x): y = x + 1; return y"
    assert classify(old, new)[0][1] == "body_or_docstring_changed"

def test_removed_symbol():
    assert classify("def old_api(): pass", "")[0][1] == "removed"
