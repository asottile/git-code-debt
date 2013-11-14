import flask
import mako.lookup

app = flask.Flask(__name__)

template_lookup = mako.lookup.TemplateLookup(
    directories=['git_code_debt_server/templates'],
)

def render_template(template_name, **env):
    template = template_lookup.get_template(template_name)
    return template.render(**env)

@app.route('/')
def index():
    return render_template('index.mako')

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
