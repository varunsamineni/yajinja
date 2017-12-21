from jinja2 import Environment, FileSystemLoader, StrictUndefined, Undefined
import yaml
import click
import os 

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
def main(input_file, template_file, environment,
    undefined, output_file):

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

    output_file = template_file[:-4]

    rendered_template = template.render(input_variables)
    print(rendered_template)

    with open(output_file, 'w') as f:
        f.write(rendered_template)

if __name__ == '__main__':
    main()