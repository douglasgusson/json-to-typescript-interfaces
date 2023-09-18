#!/usr/bin/env python3
from sys import stdin, stdout, stderr, argv
import re
import json


def python_type_to_typescript_type(py_type: str) -> str:
    """
    Converts Python type to TypeScript type.
    """
    if py_type in ["int", "float"]:
        return "number"
    elif py_type == "bool":
        return "boolean"
    elif py_type == "str":
        return "string"
    elif py_type == "list":
        return "Array<any>"
    elif py_type == "dict":
        return "any"
    else:
        return "any"


def kebab_to_camel(kebab_str: str, first_caps: bool = False) -> str:
    """
    Convert kebab-case to camelCase
    """
    first, *others = kebab_str.split("-")
    first = first_caps and first.capitalize() or first.lower()
    return "".join([first, *map(str.title, others)])


def snake_to_camel(snake_str: str, first_caps: bool = False) -> str:
    """
    Convert snake_case to camelCase
    """
    first, *others = snake_str.split("_")
    first = first_caps and first.capitalize() or first.lower()
    return "".join([first, *map(str.title, others)])


def case_normalize(string: str, first_caps: bool = False):
    if "-" in string:
        return kebab_to_camel(string, first_caps)
    elif "_" in string:
        return snake_to_camel(string, first_caps)
    return string


def check_valid_typescript_identifier(identifier: str) -> bool:
    regex = "^[$_a-zA-Z][a-zA-Z0-9_$]*$"

    if re.match(regex, identifier):
        return True
    else:
        return False


def str_json_to_typescript_interface(
    data: dict,
    interface_name: str = "IRootObject",
    apply_attr_camel_case: bool = False,
) -> str:
    """
    Convert JSON to TypeScript interface
    """
    atributos = []
    interfaces = []

    for key in data:
        py_type = type(data[key]).__name__
        typescript_type = python_type_to_typescript_type(py_type)

        if py_type == "dict":
            interfaces.append(
                str_json_to_typescript_interface(data[key], key.capitalize())
            )
            typescript_type = case_normalize(key, True)

        if py_type == "list" and len(data[key]) > 0:
            py_type = type(data[key][0]).__name__
            typescript_type = "{}[]".format(python_type_to_typescript_type(py_type))

            if py_type == "dict":
                iname = key.capitalize()[:-1]
                interfaces.append(str_json_to_typescript_interface(data[key][0], iname))
                typescript_type = "{}[]".format(case_normalize(iname, True))

        attribute_name = case_normalize(key) if apply_attr_camel_case else key

        if check_valid_typescript_identifier(attribute_name):
            atributos.append(f"  {attribute_name}: {typescript_type};\n")
        else:
            atributos.append(f"  '{attribute_name}': {typescript_type};\n")

    interfaces.append(
        "export interface {} {{\n{}}}\n".format(
            case_normalize(interface_name, True), "".join(atributos)
        )
    )

    return "\n".join(interfaces)


if __name__ == "__main__":
    try:
        _dict = json.load(stdin)
    except json.JSONDecodeError:
        stderr.write("Invalid JSON")
        exit(1)

    if len(argv) > 1 and len(argv[1]) > 0 and argv[1] not in ["0", "1"]:
        stderr.write(f"Camelize attributes: 0 or 1 expected, got {len(argv[1])}")
        exit(1)

    # camelize attributes
    apply_camelize = bool(int(argv[1])) if len(argv[1]) > 1 else False

    output_string = str_json_to_typescript_interface(
        data=_dict,
        apply_attr_camel_case=apply_camelize,
    )

    stdout.write(output_string)
