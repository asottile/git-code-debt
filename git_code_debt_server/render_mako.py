import mako.lookup

template_lookup = mako.lookup.TemplateLookup(
    directories=['git_code_debt_server/templates'],
)

def render_template(template_name, **env):
    template = template_lookup.get_template(template_name)
    return template.render(**env)
