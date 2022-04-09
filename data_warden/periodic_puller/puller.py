from apscheduler.schedulers.blocking import BlockingScheduler
from common.config import Config
from common.storage.s3_handler import S3Handler
from common.storage.postresql_handler import PostgresqlHandler

__config__ = Config()
__postgres_handler__ = PostgresqlHandler()
__s3_handler__ = S3Handler()


def pulling_job():
    print("Decorated job")


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
