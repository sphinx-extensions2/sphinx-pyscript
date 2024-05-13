"""A sphinx extension for adding pyscript to a page"""

__version__ = "0.2.0"

import json
from pathlib import Path

import yaml
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.fileutil import copy_asset_file
from sphinx.util.logging import getLogger

DEFAULT_VERSION = "2024.4.2"


def setup(app: Sphinx):
    """Setup the extension"""
    app.add_config_value(
        "pyscript_js", f"https://pyscript.net/releases/{DEFAULT_VERSION}/core.js", "env"
    )
    app.add_config_value(
        "pyscript_css",
        f"https://pyscript.net/releases/{DEFAULT_VERSION}/core.css",
        "env",
    )
    app.add_directive("py-config", PyConfig)
    app.add_directive("py-script", PyScript)
    app.add_directive("py-editor", PyEditor)
    app.add_directive("py-terminal", PyTerminal)
    app.connect("doctree-read", doctree_read)
    app.connect("html-page-context", add_html_context)
    app.connect("build-finished", copy_asset_files)
    return {"version": __version__, "parallel_read_safe": True}


LOGGER = getLogger(__name__)


class PyConfig(SphinxDirective):
    """Parse the py-config as a directive"""

    has_content = True

    def run(self):
        """Parse the config"""
        if self.content:
            try:
                config = yaml.safe_load("\n".join(self.content))
            except Exception:
                raise self.error("Could not read config as YAML")
        else:
            config = {}
        self.env.metadata[self.env.docname]["py-config"] = json.dumps(config)
        return []


class PyScript(SphinxDirective):
    """Add a py-script tag"""

    has_content = True
    option_spec = {
        "file": directives.path,
    }

    def run(self):
        """Add the py-script tag"""
        if "file" in self.options:
            path = Path(self.env.relfn2path(self.options["file"])[1])
            try:
                code = path.read_text(encoding="utf8")
            except Exception as exc:
                raise self.error(f"Could not read file: {exc}")
            self.env.note_dependency(path)
        elif self.content:
            code = "\n".join(self.content)
        else:
            raise self.error("Must provide either content or the 'file' option")
        return [
            nodes.raw("", f"<script type='py'>\n{code}\n</script>\n", format="html")
        ]


class PyEditor(SphinxDirective):
    """Add a py-editor tag"""

    has_content = True

    """
    Notes on <py-editor> options. See https://docs.pyscript.net/2024.5.2/user-guide/editor/ for details
        env: The name of a particular instance of the CPython interpreter. Cells with the same 'env' share an interpreter
        setup: designates a 'setup' tag 
        config: The URL of a PyScript configuration file (TOML or JSON), or an inline configuration
    """
    option_spec = {
        "env": directives.unchanged,
        "setup": directives.flag,
        "config": directives.unchanged,
    }

    def run(self):
        """Add the py-editor tag"""
        attrs = ""
        code = ""
        if "env" in self.options:
            attrs += f' env="{self.options["""env"""]}"'
        if "config" in self.options:
            attrs += f' config="{self.options["""config"""]}"'
        if "setup" in self.options:
            attrs += "setup"
        if self.content:
            code = "\n".join(self.content)
        return [
            nodes.raw(
                "",
                f"<script type='py-editor' {attrs}>\n{code}\n</script>\n",
                format="html",
            )
        ]


class PyTerminal(SphinxDirective):
    """Add a py-terminal tag"""

    option_spec = {}

    def run(self):
        """Add the py-terminal tag"""
        attrs = ""
        if "worker" in self.options:
            attrs += " worker"
        return [
            nodes.raw(
                "", f"<script type='py' terminal {attrs}></script>\n", format="html"
            )
        ]


def add_html_context(
    app: Sphinx, pagename: str, templatename: str, context, doctree: nodes.document
):
    """Add extra variables to the HTML template context."""
    if doctree and "pyscript" in doctree:
        app.add_js_file(app.config.pyscript_js, type="module")
        app.add_js_file("../mini-coi.js")
        app.add_css_file(app.config.pyscript_css)


def doctree_read(app: Sphinx, doctree: nodes.document):
    """Setup the doctree."""
    metadata = app.env.metadata[app.env.docname]
    if "py-config" in metadata:
        try:
            data = json.loads(metadata["py-config"])
            assert isinstance(data, dict), "must be a dictionary"
        except Exception as exc:
            LOGGER.warning(
                f"Could not parse pyscript config: {exc}", location=(app.env.docname, 0)
            )
        else:
            doctree["pyscript"] = True
            data_str = json.dumps(data, indent=2)
            doctree.append(
                nodes.raw(
                    "",
                    f'<py-config type="json">\n{data_str}\n</py-config>\n',
                    format="html",
                )
            )


def copy_asset_files(app, exc):
    if app.builder.format == "html" and not exc:
        custom_file = (Path(__file__).parent / "mini-coi.js").absolute()
        static_dir = (Path(app.builder.outdir)).absolute()
        copy_asset_file(str(custom_file), str(static_dir))
