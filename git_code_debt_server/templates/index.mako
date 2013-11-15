<%inherit file="base.mako" />

<%block name="title">Index</%block>

<%block name="css">
    <link rel="stylesheet" type="text/css" href="static/css/git_code_debt.css">
</%block>

<%block name="scripts">
    ${parent.scripts()}
    <script src="static/js/chart.js"></script>
</%block>

<h1>Technical Debt</h1>

<table>
    <tr>
        <th>Metric</th>
        <th>Value</th>
        <th>Today's Change</th>
    </tr>
    % for metric in metrics:
        <tr>
            <td><a href="${metric['href']}">${metric['title']}</a></td>
            <td>${metric['occurrences']}</td>
            <td>${metric['change']}</td>
        </tr>
    % endfor
</table>
