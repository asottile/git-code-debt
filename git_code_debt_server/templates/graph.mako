<%inherit file="base.mako" />

<%block name="title">${metric_name}</%block>

<%block name="css">
    ${parent.css()}
    <link rel="stylesheet" type="text/css" href="../static/css/git_code_debt.css">
</%block>

<%block name="scripts">
    ${parent.scripts()}
    <script src="../static/js/chart.js"></script>
    <script src="../static/js/git_code_debt.js"></script>
</%block>

<script>
    metrics = ${metrics};
</script>

<h1>${metric_name}</h1>
<canvas id="graph" width="800" height="600"></canvas>
<div class="date-picker">
    From: <input type="text" id="datepicker-from" data-timestamp="${start_timestamp}">
    To: <input type="text" id="datepicker-to" data-timestamp="${end_timestamp}">
</div>
