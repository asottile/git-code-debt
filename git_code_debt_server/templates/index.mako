<%!
import flask
%>

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
        <th>Current Value</th>
        % for time_name, _ in offsets:
            <th>${time_name}</th>
        % endfor
    </tr>

    % for metric in metric_names:
        <tr>
            <td>${metric}</td>
            <td>${current_values[metric]}</td>
            % for time_name, timestamp in offsets:
                <%
                    delta = current_values[metric] - metric_data[time_name][metric]
                    classname = 'metric-up' if delta > 0 else 'metric-down' if delta < 0 else 'metric-none'
                %>
                <td class="${classname}">
                    <a target="_blank" href="${flask.url_for(
                        'graph.show',
                        name=metric,
                        start=str(timestamp),
                        end=str(today_timestamp),
                    )}">
                        ${delta}
                    </a>
                </td>
            % endfor
        </tr>
    % endfor

</table>
