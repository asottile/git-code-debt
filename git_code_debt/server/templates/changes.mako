<%!
    import flask

    from git_code_debt.util.iter import chunk_iter
%>

%for changes_chunk in chunk_iter(changes, 10):
    <div class="changes-block">
        <table class="${override_classname}">
            <thead><th>Time</th><th>Sha</th><th>Change</th></thead>
            <tbody>${changes_rows(changes_chunk)}</tbody>
        </table>
    </div>
%endfor


<%def name="changes_rows(changes)">
    %for date_time, sha, change in changes:
        <tr>
            <td>${date_time}</td>
            <td>
                <a href="${flask.url_for('commit.show', sha=sha)}">
                    ${sha[:8]}
                </a>
            </td>
            <td class="${change.delta.classname}">
                ${change.delta.value}
            </td>
        </tr>
    %endfor
</%def>
