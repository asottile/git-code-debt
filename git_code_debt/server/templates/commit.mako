<%!
from git_code_debt.util.iter import chunk_iter
%>

<%inherit file="base.mako" />

<%block name="title">Code Debt - Commit ${short_sha}</%block>

<h1>Commit - ${short_sha}</h1>

<hr>

<table class="layout-table">
    <tr>
        <td>${render_debt_stats(commit_deltas)}</td>
        <td>${render_links(links)}</td>
    </tr>
</table>


<%def name="render_debt_stats(commit_deltas)">
    <table class="debt-stats-table">
        <thead>
            <th colspan="2"><h2>Debt stats</h2></th>
        </thead>
        <tbody>
            %for commit_delta in commit_deltas:
                <tr class="${commit_delta.classname}">
                    <th>${commit_delta.metric_name}</th>
                    <td class="${commit_delta.delta.classname}">
                        ${commit_delta.delta.value}
                    </td>
                </tr>
            %endfor
        </tbody>
    </table>
</%def>


<%def name="render_links(links)">
    <h2>Links</h2>
    <ul>
        %for link_text, link_url in links:
            <li><a href="${link_url}" target="_blank">${link_text}</a></li>
        %endfor
    </ul>
</%def>
