"""
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
    --delete                                           Delete files after templating them out. No effect if --standard-out
    --allow-undefined -u                               Allow undefined variables to be templated as empty strings
"""
import os
import sys
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, Undefined
from docopt import docopt


def main(input_file, template_file, environment,
         undefined, output_file, std_out, directory, delete):
    """
    Proccesses Command line arguments, variables, and then templates
    out the file
    """

    if not directory and not template_file:
        raise Exception('--directory or --template-file need to be specified')

    if directory and output_file:
        raise Exception('--output-file is not compatible with --directory')

    # If output file is not specified, we set output_file to template_file sans extension
    # this should we do this below when looping over a directory
    # TODO DRY this up with directory
    if template_file and len(template_file.split('.')) < 2 and not output_file:
        raise Exception('template file needs an extension if output file is not specified')
    elif template_file and not output_file:
        extension_len = len(template_file.split('.')[-1]) + 1
        output_file = template_file[:-extension_len]


    if undefined:
        undefined = Undefined
    else:
        undefined = StrictUndefined

    variables = process_variables(input_file, environment)

    if directory:
        template_files = [f for f in os.listdir(directory) if f.endswith('.tpl')]
        if not template_files:
            raise Exception(f'no template files found in {directory} directory')
        for file in template_files:
            template_file = f'{directory}/{file}'
            output_file = f'{directory}/{file}'[:-4]
            process_template(template_file, output_file, variables, undefined, std_out, delete)
    else:
        process_template(template_file, output_file, variables, undefined, std_out, delete)


def process_template(template_file, output_file, variables, undefined, std_out, delete):
    """
    Processes a jinja template with specified variables
    either writes them to stdout, or to specififed files based
    on user preference
    """

    loader = FileSystemLoader(searchpath='.')
    env = Environment(loader=loader, undefined=undefined, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_file)

    rendered_template = template.render(variables)
    if std_out:
        print(template_file)
        print('--------------')
        print(rendered_template)
    else:
        with open(output_file, 'w') as f:
            f.write(rendered_template)
        if delete:
            os.remove(template_file)


def process_variables(input_file, environment):
    """
    Creates a dict of variables to pass through
    to jinja. If both environment variables and
    input file variables are specififed, we merge
    and prefer input variables.
    """
    input_variables = {}
    env_variables = {}

    if not input_file:
        environment = True
    if input_file:
        input_variables = yaml.load(open(input_file))
    if environment:
        env_variables = dict([(k, v) for k, v in os.environ.items()])

    return {**env_variables, **input_variables}

def cli():
    """
    calls main function with cli options
    """
    arguments = docopt(__doc__, version='yajinja 0.0.1')
    main(arguments['--input-file'], arguments['--template-file'],
         arguments['--environment'], arguments['--allow-undefined'],
         arguments['--output-file'], arguments['--standard-out'],
         arguments['--directory'], arguments['--delete'])

if __name__ == '__main__':
    cli()

