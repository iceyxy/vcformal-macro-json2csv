# vcformal-macro-json2csv
A macro-aware conversion tool for translating JSON configuration files to CSV format, optimized for VC Formal verification flows.
## Overview
This utility specializes in processing JSON files containing macro references (SystemVerilog-style `define` syntax) and converting them into structured CSV outputs. It handles recursive expansion of nested macros, making it ideal for generating verification constraints, connection matrices, and configuration tables for VC Formal environments.

## Key Features
- Recursive nested macro expansion
- JSON to CSV conversion with Jinja2 templating
- Support for VC Formal verification workflows
- Debug mode for validating macro expansion chains
- Preservation of hierarchical design paths through macro resolution

## Usagepython main.py --json <input.json> --template <template.j2> --output <output.csv> --macro <macros.sv> [--debug]
## Use Cases
- Generating VC Formal constraint files from high-level JSON configs
- Resolving macro-based hierarchical paths in design verification
- Automating testbench configuration translation
- Converting macro-rich verification intent to machine-readable CSV

## Dependencies
- Python 3.x
- Jinja2
