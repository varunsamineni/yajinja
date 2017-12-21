"""
Usage:
  yajinja [--input-file=<input_file> --output-file=<output_file>]
          [--directory=<directory> | --template-file=<template_file>]
          [options]
  yajinja [--help -h --version]

Options:
    --input-file=<input_file> -i=<input_file>          Path to the input file
    --output-file=<output_file> -o=<output_file>       Path to the output file
    --directory=<directory> -d=<directory>             Path to directory containging *.tpl files
    --template-file=<template_file> -t=<template_file> Path to a single template file
    --standard-out -s                                  Print rendered templates to standard out
    --environment -e                                   Concider Enivronment Variables when templating
    --allow-undefined -u                               Allow undefined variables to be templated as empty strings
"""
import os
import sys
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, Undefined
from docopt import docopt


def main(input_file, template_file, environment,
         undefined, output_file, std_out, directory):

    # Directory and template file are mutually exclusive.
    # output file is not compatible with directory.
    if directory and template_file:
        print('--directory and --input-file are mutually exclusive.')
        sys.exit(1)
    
    if not directory and not template_file:
        print('--directory or --template-file need to be specified')
        sys.exit(1)

    if directory and output_file:
        print('--output-file is not compatible with --directory')
        sys.exit(1)

    if template_file and len(template_file.split('.')) < 2 and not output_file:
        print('template file needs an extension if output file is not specified')
        sys.exit(1)
    elif template_file and not output_file:
        extension_len = len(template_file.split('.')[-1]) + 1
        output_file = template_file[:-extension_len]

    if undefined:
        undefined = Undefined
    else:
        undefined = StrictUndefined

    # proccess variables
    variables = process_variables(input_file, environment)
    # Proccess template
    if directory:
        [process_template(directory + '/' + i, directory + '/' + i[:-4], variables, undefined, std_out) for i in os.listdir(directory) if i.endswith('.tpl')]
    else:
        process_template(template_file, output_file, variables, undefined, std_out)


def process_template(template_file, output_file, variables, undefined, std_out):
    loader = FileSystemLoader(searchpath='.')
    env = Environment(loader=loader, undefined=undefined, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_file)

    rendered_template = template.render(variables)
    if std_out:
        print('-------------')
        print(template_file)
        print(rendered_template)
    else:
        with open(output_file, 'w') as f:
            f.write(rendered_template)


def process_variables(input_file, environment):
    input_variables = {}
    env_variables = {}
    if not input_file:
        environment = True
    if input_file:
        input_variables = yaml.load(open(input_file))
    if environment:
        env_variables = dict([(k, v) for k, v in os.environ.items()])

    return {**env_variables, **input_variables}

if __name__ == '__main__':
    cli()

def cli():
    arguments = docopt(__doc__, version='yajinja 0.0.1')
    main(arguments['--input-file'], arguments['--template-file'],
         arguments['--environment'], arguments['--allow-undefined'],
         arguments['--output-file'], arguments['--standard-out'],
         arguments['--directory'])