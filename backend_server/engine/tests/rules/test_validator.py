from main.rules.validator import FormatValidator

def test_valid_action():
    data = {
        "type" : "board",
        "pos" : [1, 1]
    }

    assert FormatValidator().is_valid_action(data)

def test_invalid_action():
    data = {
        "type" : "board",
        "pos" : 1
    }

    assert not FormatValidator().is_valid_action(data)

def test3():
    data = {
        "type" : "hand",
        "slot" : 0
    }

    assert FormatValidator().is_valid_action(data)

