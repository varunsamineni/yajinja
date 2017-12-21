import sys
from context import yajinja
import os


def test_env_vars_only():
    vars = {'FOO':'ZING'}
    os.environ.update(vars)
    input_file = None
    environment = True
    r = yajinja.cli.process_variables(input_file, environment)
    assert r.get('FOO') == 'ZING'

def test_input_file_only():
    input_file = './tests/test-input.yml'
    environment = False
    r = yajinja.cli.process_variables(input_file, environment)
    assert r.get('baz') == 'bar'

def test_env_and_input():
    input_file = './tests/test-input.yml'
    vars = {'FOO':'ZING'}
    environment = True
    os.environ.update(vars)
    r = yajinja.cli.process_variables(input_file, environment)
    assert r.get('FOO') == 'ZING'
    assert r.get('baz') == 'bar'
