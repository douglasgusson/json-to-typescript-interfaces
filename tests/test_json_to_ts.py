from json_to_ts import (
    snake_to_camel,
    kebab_to_camel,
    case_normalize,
    python_type_to_typescript_type,
    check_valid_typescript_identifier,
)


def test_snake_to_camel():
    assert snake_to_camel("hello_world") == "helloWorld"


def test_snake_to_camel_with_first_caps():
    assert snake_to_camel("hello_world", True) == "HelloWorld"


def test_snake_to_camel_with_every_caps():
    assert snake_to_camel("HELLO_WORLD") == "helloWorld"


def test_snake_to_camel_with_every_caps_and_first_caps():
    assert snake_to_camel("HELLO_WORLD", True) == "HelloWorld"


def test_kebab_to_camel():
    assert kebab_to_camel("hello-world") == "helloWorld"


def test_kebab_to_with_first_caps():
    assert kebab_to_camel("hello-world", True) == "HelloWorld"


def test_case_normalize():
    assert case_normalize("hello_world") == "helloWorld"
    assert case_normalize("hello-world") == "helloWorld"


def test_python_type_to_typescript_type_int():
    assert python_type_to_typescript_type("int") == "number"


def test_python_type_to_typescript_type_float():
    assert python_type_to_typescript_type("float") == "number"


def test_python_type_to_typescript_type_bool():
    assert python_type_to_typescript_type("bool") == "boolean"

def test_check_valid_typescript_identifier_starts_with_invalid_char():
    assert check_valid_typescript_identifier('@id') == False
    assert check_valid_typescript_identifier('1d') == False

def test_check_valid_typescript_identifier_starts_with_valid_char():
    assert check_valid_typescript_identifier('$id') == True
    assert check_valid_typescript_identifier('_id') == True

def test_check_valid_typescript_basic_identifier():
    assert check_valid_typescript_identifier('id') == True
