= Automatic documentation
To automatically generate documentation from docstrings in your code, you can use the `sphinx-apidoc` tool. This tool will create reStructuredText files for each module in your codebase, which can then be included in your Sphinx documentation.
```bash
sphinx-apidoc -o docs/source/ code/
```

== usage in .rst
```rst
.. automodule:: mymodule
   :members:
```

