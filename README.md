# yajinja

Render jinja2 templates from input-files, or from environment variables

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


## Authors
* **Dann Bohn** (https://github.com/whereismyjetpack)

