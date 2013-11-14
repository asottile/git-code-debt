<%inherit file="base.mako" />

<%block name="title">Index</%block>

<%block name="css">
    <link rel="stylesheet" type="text/css" href="static/css/git_code_debt.css">
</%block>

<%block name="scripts">
    ${parent.scripts()}
    <script src="static/js/chart.js"></script>
    <script src="static/js/git_code_debt.js"></script>
</%block>

<canvas id="graph" width="800" height="600"></canvas>
