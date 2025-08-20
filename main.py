#!/usr/bin/env python3
"""
FILE NAME    : main.py
DESCRIPTION  : Tool to process JSON data with macro expansion using Jinja2 templates
"""

import re
import json
import argparse
from jinja2 import Environment, FileSystemLoader


class ConfigItem:
    """Class to encapsulate JSON data records"""
    def __init__(self, ENABLE="", SOURCE="", DESTINATION="", NAME=""):
        self.ENABLE = ENABLE
        self.SOURCE = SOURCE
        self.DESTINATION = DESTINATION
        self.NAME = NAME


def extract_macros(macro_text):
    """Extract raw macros from definition text without expansion"""
    pattern = re.compile(
        r"`define\s+(\w+)\s+(.*?)(?=\s*`define|$)", 
        re.DOTALL | re.MULTILINE
    )
    macros = {}
    for name, value in pattern.findall(macro_text):
        cleaned = re.sub(r"//.*", "", value)  # Remove comments
        cleaned = re.sub(r"\s+", " ", cleaned).strip()  # Normalize whitespace
        macros[name] = cleaned
    return macros


def expand_value(value, macros, depth=0):
    """Recursively expand macro references in a value string"""
    MAX_DEPTH = 1000
    if depth >= MAX_DEPTH:
        print(f"Warning: Reached max expansion depth ({MAX_DEPTH}) for value: {value[:50]}...")
        return value

    macro_refs = re.findall(r"`(\w+)", value)
    if not macro_refs:
        return value

    expanded_value = value
    for ref in macro_refs:
        if ref not in macros:
            continue
        expanded_value = re.sub(rf"`{ref}\b", macros[ref], expanded_value)

    return expand_value(expanded_value, macros, depth + 1)


def expand_object_attributes(obj, macros):
    """Expand macros in all attributes of a ConfigItem object"""
    obj.ENABLE = expand_value(obj.ENABLE, macros)
    obj.SOURCE = expand_value(obj.SOURCE, macros)
    obj.DESTINATION = expand_value(obj.DESTINATION, macros)
    obj.NAME = expand_value(obj.NAME, macros)
    return obj


def json_to_objects(json_path, macros):
    """Convert JSON file to list of ConfigItem objects with macro expansion"""
    with open(json_path, "r") as f:
        json_data = json.load(f)

    objects = []
    for item in json_data:
        config_obj = ConfigItem(
            ENABLE=item.get("ENABLE", ""),
            SOURCE=item.get("SOURCE", ""),
            DESTINATION=item.get("DESTINATION", ""),
            NAME=item.get("NAME", "")
        )
        objects.append(config_obj)

    return [expand_object_attributes(obj, macros) for obj in objects]


def render_template(objects, template_path, output_path):
    """Render objects using Jinja2 template and save to output file"""
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_path)
    context = {"items": objects}
    rendered_content = template.render(context)
    
    with open(output_path, "w") as f:
        f.write(rendered_content)


def main():
    """Main function to parse arguments and execute processing"""
    parser = argparse.ArgumentParser(
        description="Process JSON data with macro expansion and render using Jinja2"
    )
    parser.add_argument("--json", required=True, help="Input JSON file path")
    parser.add_argument("--template", required=True, help="Jinja2 template file path")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--macro", required=True, help="Macro definition file path")
    parser.add_argument("--debug", action="store_true", help="Show debugging information")

    args = parser.parse_args()

    # Extract macros
    with open(args.macro, "r") as f:
        macros = extract_macros(f.read())

    if args.debug:
        print("Raw macros:")
        for name, val in macros.items():
            print(f"`define {name} {val}")
        print()

    # Create and expand objects
    objects = json_to_objects(args.json, macros)

    if args.debug:
        print("Expanded objects:")
        for i, obj in enumerate(objects):
            print(f"Object {i + 1}:")
            print(f"  ENABLE: {obj.ENABLE}")
            print(f"  SOURCE: {obj.SOURCE}")
            print(f"  DESTINATION: {obj.DESTINATION}")
            print(f"  NAME: {obj.NAME}")
        print()

    # Render output
    render_template(objects, args.template, args.output)
    print(f"Output saved to {args.output}")


if __name__ == "__main__":
    main()
