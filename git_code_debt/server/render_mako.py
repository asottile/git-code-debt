from __future__ import absolute_import
from __future__ import unicode_literals

import mako.lookup
import pkg_resources


template_lookup = mako.lookup.TemplateLookup(
    directories=[
        pkg_resources.resource_filename('git_code_debt.server', 'templates'),
    ],
)


def render_template(template_name, **env):
    template = template_lookup.get_template(template_name)
    return template.render(**env)
