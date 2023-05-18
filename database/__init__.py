import aiomysql
from aiomysql.pool import create_pool

from configs.settings import settings


pool = None


async def get_pool() -> aiomysql.pool.Pool:
    global pool

    if pool is not None and not pool.closed:
        return pool

    try:
        pool = await create_pool(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            db=settings.DB_NAME,
            port=int(settings.DB_PORT),
            autocommit=True,
            minsize=1,
            maxsize=10,
        )
    except aiomysql.OperationalError as e:
        print("Unable to connect to database:", e)
        raise e

    return pool


async def db_shutdown():
    global pool
    if pool is not None:
        pool.close()
        await pool.wait_closed()


async def db_connect():
    # Get Connection from Pool
    pool = await get_pool()
    conn = await pool.acquire()
    try:
        await conn.ping()
        return conn
    except aiomysql.OperationalError as e:
        print("Unable to connect to database:", e)
        raise e
    finally:
        pool.release(conn)
