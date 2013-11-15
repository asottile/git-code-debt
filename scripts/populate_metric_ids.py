
from git_code_debt_server.app import get_database
from git_code_debt_server.logic.metrics import get_metric_ids

def main():
    with get_database() as database:
        metric_ids = get_metric_ids()

        for metric_id in metric_ids:
            database.execute(
                "INSERT INTO metric_names ('name') VALUES (?)", [metric_id]
            )

if __name__ == '__main__':
    main()
