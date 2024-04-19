"""A sphinx extension for adding pyscript to a page"""

__version__ = "0.1.0"

import json
import os
from pathlib import Path

import yaml
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.logging import getLogger


def setup(app: Sphinx):
    """Setup the extension"""
    app.add_config_value(
        "pyscript_js", "https://pyscript.net/releases/2022.12.1/pyscript.js", "env"
    )
    app.add_config_value(
        "pyscript_css", "https://pyscript.net/releases/2022.12.1/pyscript.css", "env"
    )
    app.add_directive("py-config", PyConfig)
    app.add_directive("py-script", PyScript)
    app.add_directive("py-repl", PyRepl)
    app.add_directive("py-terminal", PyTerminal)
    app.connect("doctree-read", doctree_read)
    app.connect("html-page-context", add_html_context)
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
        return [nodes.raw("", f"<py-script>\n{code}\n</py-script>\n", format="html")]


class PyRepl(SphinxDirective):
    """Add a py-repl tag"""

    has_content = True
    option_spec = {
        "auto-generate": directives.flag,
        "output": directives.unchanged,
    }

    def run(self):
        """Add the py-repl tag"""
        attrs = ""
        code = ""
        if "auto-generate" in self.options:
            attrs += ' auto-generate="true"'
        if "output" in self.options:
            attrs += f' output="{self.options["output"]}"'
        if self.content:
            code = "\n".join(self.content)
        return [nodes.raw("", f"<py-repl{attrs}>\n{code}\n</py-repl>\n", format="html")]


class PyTerminal(SphinxDirective):
    """Add a py-terminal tag"""

    option_spec = {
        "auto": directives.flag,
    }

    def run(self):
        """Add the py-terminal tag"""
        attrs = ""
        if "auto" in self.options:
            attrs += " auto"
        return [nodes.raw("", f"<py-terminal{attrs}></py-terminal>\n", format="html")]


def add_html_context(
    app: Sphinx, pagename: str, templatename: str, context, doctree: nodes.document
):
    """Add extra variables to the HTML template context."""
    if doctree and "pyscript" in doctree:
        app.add_js_file(app.config.pyscript_js, loading_method="defer")
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
            _copy_wheels(app, data)
            data_str = json.dumps(data, indent=2)
            doctree.append(
                nodes.raw(
                    "",
                    f'<py-config type="json">\n{data_str}\n</py-config>\n',
                    format="html",
                )
            )


def _copy_wheels(app: Sphinx, data: dict) -> None:
    """Copy wheels to the output directory."""
    packages = []
    for pkg in data.get("packages", []):
        if pkg.endswith(".whl"):
            rel_filename, filename = app.env.relfn2path(pkg, app.env.docname)
            app.env.dependencies[app.env.docname].add(rel_filename)
            if not os.access(filename, os.R_OK):
                LOGGER.warning(
                    f"Could not read pyscript wheel: {filename}",
                    location=(app.env.docname, 0),
                )
                continue
            packages.append(
                "_downloads/" + app.env.dlfiles.add_file(app.env.docname, rel_filename)
            )
        else:
            packages.append(pkg)
    if packages:
        data["packages"] = packages
