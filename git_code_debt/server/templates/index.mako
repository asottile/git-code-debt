<%!
from git_code_debt.server.servlets.index import DATE_NAMES_TO_TIMEDELTAS
%>

<%inherit file="base.mako" />

<%block name="title">Code Debt - Index</%block>

<%block name="scripts">
    ${parent.scripts()}
    <script src="/static/js/index.js"></script>
</%block>

<h1>Technical Debt</h1>

<table>
    <thead>
        <th class="dummy-cell"></th>
        <th>Metric</th>
        <th>Current Value</th>
        % for time_name, _ in DATE_NAMES_TO_TIMEDELTAS:
            <th>${time_name}</th>
        % endfor
    </thead>
    % for group in groups:
        <% first = True %>
        <tbody data-group="${group.name}" class="expanded">
            % for metric in group.metrics:
                <tr class="${metric.classname}">
                    % if first:
                        <% first = False %>
                        <th class="group-name" rowspan="${len(group.metrics)}">
                            ${group.name}
                        </th>
                    % endif
                    <td><a href="${metric.all_data_url}">${metric.name}</a></td>
                    <td>${metric.current_value}</td>
                    % for delta in metric.historic_deltas:
                        <td class="${delta.classname}">
                            <a target="_blank" href="${delta.url}">
                                ${delta.value}
                            </a>
                        </td>
                    % endfor
                </tr>
            % endfor
            <tr class="dummy-row">
                <th class="group-name">
                    ${group.name}
                </th>
                <td
                    class="dummy-cell"
                    rowspan="${len(group.metrics)}"
                    colspan="${len(DATE_NAMES_TO_TIMEDELTAS) + 2}"
                ></td>
            </tr>
        </tbody>
    % endfor
</table>
