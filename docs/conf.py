from datetime import date

from sphinx_pyscript import __version__

# -- Project information -----------------------------------------------------

project = "Sphinx PyScript"
version = __version__
copyright = f"{date.today().year}, Chris Sewell"
author = "Chris Sewell"

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "sphinx_pyscript",
]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
myst_enable_extensions = ["deflist"]

# -- HTML output -------------------------------------------------

html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/chrisjsewell/sphinx_pyscript/",
    "source_branch": "main",
    "source_directory": "docs/",
}
