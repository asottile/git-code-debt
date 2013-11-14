import flask
import mako.lookup
import os.path

app = flask.Flask(__name__)

template_lookup = mako.lookup.TemplateLookup(
    directories=['git_code_debt_server/templates'],
)

APP_ROOT = os.path.abspath(os.path.dirname(__file__))

def render_template(template_name, **env):
    template = template_lookup.get_template(template_name)
    return template.render(**env)

@app.route('/')
def index():
    return render_template('index.mako')

EXTENSIONS_TO_MIMETYPES = {
    '.js': 'application/javascript',
    '.html': 'text/html',
}

STATIC_DIR = 'static'

EXTENSIONS_TO_STATIC_DIRS = {
    '.js': 'static/js',
    '.html': 'static/html',
}

assert set(EXTENSIONS_TO_MIMETYPES.keys()) == set(EXTENSIONS_TO_STATIC_DIRS.keys())

@app.route('/<path:path>')
def catch_all(path):
    if not app.debug:
        flask.abort(404)

    if not any(
        path.endswith(extension)
        for extension in EXTENSIONS_TO_MIMETYPES.keys()
    ):
        flask.abort(404)

    extension = os.path.splitext(path)[1]

    try:
        file_path = os.path.join(
            APP_ROOT,
            EXTENSIONS_TO_STATIC_DIRS[extension],
            path,
        )

        if not file_path.startswith(os.path.join(APP_ROOT, STATIC_DIR)):
            flask.abort(404)

        with open(file_path) as asset_file:
            return flask.Response(
                 asset_file.read(),
                 mimetype=EXTENSIONS_TO_MIMETYPES[extension],
            )
    except IOError:
        flask.abort(404)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
