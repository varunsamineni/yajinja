from jinja2 import Environment, FileSystemLoader, StrictUndefined, Undefined
import yaml
import click
import os 
import sys

@click.command()
@click.option('--input-file', '-i',
    help="Input file to pass to the template")
@click.option('--environment', '-e', is_flag=True, 
    help="Concider Environment variables in template")
@click.option('--template-file', '-t',
    help="Path to the template file", required=True)
@click.option('--undefined', '-u', is_flag=True,
    help="Allow Undefined Variables, Undefined variables evaluate to empty strings")
@click.option('--output-file', '-o', default=None,
    help="If specified, ouput to this file, else we will output to input_file without the extension")
@click.option('--std-out', '-s', is_flag=True,
    help="don't write out template file, print to standard out instead")
def main(input_file, template_file, environment,
    undefined, output_file, std_out):

    if len(template_file.split('.')) < 2 and not output_file:
        print('template file needs an extension if output file is not specified')
        sys.exit(1)
    else:
        extension_len = len(template_file.split('.')[-1]) + 1

    if undefined:
        undefined = Undefined
    else:
        undefined = StrictUndefined

    input_variables = yaml.load(open(input_file))
    loader = FileSystemLoader(searchpath='.')
    env = Environment(loader=loader, undefined=undefined, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_file)

    if environment:
        env_variables = dict([(k, v) for k, v in os.environ.items()])
        input_variables = {**env_variables, **input_variables}

    if not output_file:
        output_file = template_file[:-extension_len]

    rendered_template = template.render(input_variables)
    if std_out:
        print(rendered_template)
    else:
        with open(output_file, 'w') as f:
            f.write(rendered_template)

if __name__ == '__main__':
    main()