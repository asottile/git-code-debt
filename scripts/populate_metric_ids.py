
from git_code_debt.discovery import get_metric_parsers
from git_code_debt_server.app import get_database

def main():
    with get_database() as database:
        metric_ids = []
        metric_parsers = get_metric_parsers()
        for metric_parser_cls in metric_parsers:
            for metric_id in metric_parser_cls().get_possible_metric_ids():
                metric_ids.append(metric_id)

        for metric_id in metric_ids:
            database.execute(
                "INSERT INTO metric_names ('name') VALUES (?)", [metric_id]
            )

if __name__ == '__main__':
    main()
