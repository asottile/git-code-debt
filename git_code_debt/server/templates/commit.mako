<%!
from git_code_debt.util.iter import chunk_iter
%>

<%inherit file="base.mako" />

<%block name="title">Code Debt - Commit ${short_sha}</%block>

<h1>Commit - ${short_sha}</h1>


<table class="debt-stats-table">
    <thead>
        <th colspan="2"><h2>Debt stats</h2></th>
    </thead>
    <tbody>
        %for commit_delta in diff_values:
            <tr class="${commit_delta.classname}">
                <th>${commit_delta.metric_name}</th>
                <td class="${commit_delta.delta.classname}">
                    ${commit_delta.delta.value}
               </td>
            </tr>
        %endfor
    </tbody>
</table>
