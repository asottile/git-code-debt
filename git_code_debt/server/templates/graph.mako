<%inherit file="base.mako" />

<%!
    import flask
    import markdown_code_blocks
    import markupsafe

    from git_code_debt.util.iter import chunk_iter
%>

<%block name="title">Graph - ${metric_name}</%block>

<%block name="scripts">
    ${parent.scripts()}
    <script src="/static/js/jquery.flot.min.js"></script>
    <script src="/static/js/jquery.flot.selection.min.js"></script>
    <script src="/static/js/jquery.flot.time.min.js"></script>
    <script src="/static/js/graph.js"></script>
</%block>

<script>
    metrics = ${metrics};
</script>

<h1>${metric_name}</h1>
<div id="graph" style="width: 900px; height: 600px;"></div>
<div class="date-picker">
    <form action="${flask.url_for('graph.all_data', metric_name=metric_name)}" method="GET" style="display: inline-block">
       <input type="submit" value="All Data">
    </form>
</div>

<div class="description">
    ${markupsafe.Markup(markdown_code_blocks.highlight(description))}
</div>

<h2>Changes</h2>
<div class="changes-container" data-ajax-url="${changes_url}">
    <img src="/static/img/loading.gif" alt="Loading...">
</div>
