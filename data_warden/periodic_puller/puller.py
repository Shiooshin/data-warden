from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import date
from common.config import Config
from common.storage.s3_handler import S3Handler
from common.storage.postresql_handler import PostgresqlHandler

__config__ = Config()
__postgres_handler__ = PostgresqlHandler()
__s3_handler__ = S3Handler()

__today_date__ = date.today().strftime("%Y-%m-%d")


def pulling_job():
    print("Decorated job")

    if not __postgres_handler__.has_today_etl():
        pour_data()


def pour_data(date=__today_date__):
    if pour_repos(date) and pour_statistics(date):
        status = 'SUCCESS'
    else:
        status = 'ERROR'
    update_etl_status(date, status)


def update_etl_status(date, result_status):
    values = {"agg_date": date, "status": result_status}
    __postgres_handler__.write_etl_batch(date, values)


def pour_statistics(date):
    try:
        data = __s3_handler__.read_statistics_batch(date)
        __postgres_handler__.write_statistics_batch(date, data)
    except Exception:
        print('Could not pour statistics data from S3 into Postgres')
        return False


def pour_repos(date):
    try:
        data = __s3_handler__.read_repository_batch(date)
        __postgres_handler__.write_repository_batch(date, data)
    except Exception:
        print('Could not pour repository data from S3 into Postgres')


def get_scheduler():

    scheduler = BlockingScheduler()
    scheduler.add_job(pulling_job, 'interval', seconds=3)

    return scheduler


def run_scheduler():
    scheduler = get_scheduler()
    scheduler.start()


def check_connections():
    if __s3_handler__.connection_established() and __postgres_handler__.connection_established():
        pass
    else:
        print('There was an error establishing conenction to S3 or PostgreSQL. Look at logs above')
        quit()


if __name__ == "__main__":
    check_connections()

    try:
        run_scheduler()
    except (KeyboardInterrupt, SystemExit):
        pass
