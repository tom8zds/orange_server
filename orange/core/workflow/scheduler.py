from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from orange.core.database.database import SQLITE_URI

def func(name):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now + f" Hello world, {name}")

interval_task = {
    # 配置存储器
    "jobstores": {
        # 使用Redis进行存储
        'default': SQLAlchemyJobStore(SQLITE_URI)
    },
    # 配置执行器
	"executors": {
	    # 使用进程池进行调度，最大进程数是10个
	    'default': ThreadPoolExecutor(20)
	},
    # 创建job时的默认参数
    "job_defaults": {
        'coalesce': False,  # 是否合并执行
        'max_instances': 3,  # 最大实例数
    }

}
scheduler = AsyncIOScheduler(**interval_task)

scheduler.remove_all_jobs()