from nosql_db import NoSqlDB
from clearml import Task, Logger

def query_data_warehouse(db: NoSqlDB, with_clearml: bool = True):
    if with_clearml:
        task = Task.init(project_name="RAG Project", task_name="Query data warehouse")
    result = list(db.find_all())
    if with_clearml:
        logger = Logger.current_logger()
        logger.console_handlers = []
        logger.report_text(f"Query data warehouse success, documents count: {len(result)}")
        task.close()
    return result

