# Sphinx PyScript

![GitHub Repo stars](https://img.shields.io/github/stars/chrisjsewell/sphinx-pyscript?label=Like%20and%20Share%21&style=social)

This is a Sphinx extension that allows you to use [PyScript](https://docs.pyscript.net) in your documentation.

```{toctree}
:hidden:
example_md
example_rst
```

## Installation

Install with pip:

```bash
pip install sphinx-pyscript
```

## Usage

Add the extension to your `conf.py`:

```python
extensions = [
    "sphinx_pyscript",
]
```

To load PyScript on a page, either use the `py-config` directive to load the [config](https://docs.pyscript.net/latest/reference/elements/py-config.html#) in YAML format:

```restructuredtext
.. py-config::

    splashscreen:
        autoclose: true
    packages:
    - matplotlib
```

or with MyST, use the top-matter:

```yaml
---
py-config:
  splashscreen:
    autoclose: true
  packages:
  - matplotlib
---
```

See the examples for more details.

## Configuration

The extension has the following configuration options:

pyscript_js
: The URL for the PyScript JavaScript file

pyscript_css
: The URL for the PyScript CSS file
