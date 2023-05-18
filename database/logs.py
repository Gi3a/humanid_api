async def create_log(pool, log):
    sql = ''' INSERT INTO logs(human_id, operation, ip_address, device, date_create)
              VALUES(%d, %s, %s,%s, NOW()) '''
    async with pool.cursor() as cursor:
        await cursor.execute(sql, log)
        await pool.commit()
        return cursor.lastrowid
