from __future__ import annotations

import importlib.resources
from typing import Any

import mako.lookup
from mako.template import Template


class ImportlibResourcesLookup(mako.lookup.TemplateCollection):
    def __init__(self, mod: str) -> None:
        self.mod = mod
        self._cache: dict[str, Template] = {}

    def get_template(
            self,
            uri: str,
            relativeto: str | None = None,
    ) -> Template:
        if relativeto is not None:
            raise NotImplementedError(f'{relativeto=}')

        try:
            return self._cache[uri]
        except KeyError:
            pth = importlib.resources.files(self.mod).joinpath(uri)
            with importlib.resources.as_file(pth) as pth:
                return Template(
                    filename=str(pth),
                    lookup=self,
                    default_filters=['html_escape'],
                    imports=['from mako.filters import html_escape'],
                )


template_lookup = ImportlibResourcesLookup('git_code_debt.server.templates')


def render_template(template_name: str, **env: Any) -> str:
    template = template_lookup.get_template(template_name)
    return template.render(**env)
