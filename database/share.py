async def create_share(pool, share):
    sql = ''' INSERT INTO shares(human_id, shared_id, receiver, data, date_create, date_update)
              VALUES(%s, %s, %s, %s, NOW(), NOW()) '''
    async with pool.cursor() as cursor:
        await cursor.execute(sql, share)
        await pool.commit()
        return cursor.lastrowid


async def update_share(pool, share):
    sql = ''' UPDATE shares
              SET data = %s, receiver = %s, date_update = NOW() WHERE human_id = %s AND shared_id = %s '''
    try:
        async with pool.cursor() as cursor:
            await cursor.execute(sql, share)
            await pool.commit()
            return cursor.rowcount, None

    except AttributeError as e:
        return 0, str(e)


async def delete_share(pool, share):
    sql = ''' DELETE FROM shares WHERE human_id = %s AND shared_id = %s '''
    try:
        async with pool.cursor() as cursor:
            await cursor.execute(sql, share)
            await pool.commit()
            return cursor.rowcount, None

    except AttributeError as e:
        return 0, str(e)


async def get_share(pool, share_group):
    sql = ''' SELECT * FROM shares WHERE human_id = %s AND shared_id = %s '''
    try:
        async with pool.cursor() as cursor:
            await cursor.execute(sql, (share_group['id'], share_group['public_key']))
            rows = await cursor.fetchall()
            return rows

    except Exception as e:
        return 0, str(e)


async def get_shares(pool, shared_id):
    sql = ''' SELECT * FROM shares WHERE human_id = %s '''
    try:
        async with pool.cursor() as cursor:
            await cursor.execute(sql, (shared_id))
            rows = await cursor.fetchall()
            return rows

    except Exception as e:
        return 0, str(e)


async def get_accesses(pool, shared_id):
    sql = ''' SELECT * FROM shares WHERE shared_id = %s '''
    try:
        async with pool.cursor() as cursor:
            await cursor.execute(sql, (shared_id))
            rows = await cursor.fetchall()
            return rows

    except Exception as e:
        return 0, str(e)


async def get_access(pool, share_group):
    sql = ''' SELECT * FROM shares WHERE human_id = %s AND shared_id = %s '''
    try:
        async with pool.cursor() as cursor:
            await cursor.execute(sql, (share_group['human_public_key'], share_group['share_public_key']))
            rows = await cursor.fetchall()
            return rows

    except Exception as e:
        return 0, str(e)
