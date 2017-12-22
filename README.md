# yajinja

Render jinja2 templates from input-files, or from environment variables.

### Prerequisites
- Python 3.6 

## Installation 
`python setup.py install`

## Examples
1.) take a folder of templates and render them to stdout

`yajinja --directory templates --input-file vars.yaml --standard-out`

2.) take a folder of *.tpl files and render them to their name sans extension

`yajinja --directory templates --input-file vars.yaml`

3.) take a single template file and render it to a new file

`yajinja --template-file templates/test.tpl --input-file vars.yaml --output-file /tmp/foo`

4.) take a template file, and use enironment variables instead of input file

`yajinja --template-file temlates/test.tpl --environment`

## Usage
```
Usage:
  yajinja [--input-file=<input_file> --output-file=<output_file>]
          [--directory=<directory> | --template-file=<template_file>]
          [options]
  yajinja [--help -h --version]

Options:
    --input-file=<input_file> -i=<input_file>          Path to the input file
    --output-file=<output_file> -o=<output_file>       Path to the output file
    --directory=<directory> -d=<directory>             Path to directory containing *.tpl files
    --template-file=<template_file> -t=<template_file> Path to a single template file
    --standard-out -s                                  Print rendered templates to standard out
    --environment -e                                   Consider Enivronment Variables when templating
    --allow-undefined -u                               Allow undefined variables to be templated as empty strings
```


![alt text](https://i.chzbgr.com/full/6735287808/h09CE3973/ "A Ninja")

## Authors
* **Dann Bohn** (https://github.com/whereismyjetpack)

