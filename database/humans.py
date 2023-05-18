async def create_human(pool, human):
    sql = ''' INSERT INTO humans(public_key, face_encodings, date_create, date_update)
              VALUES(%s,%s, NOW(), NOW()) '''
    async with pool.cursor() as cursor:
        await cursor.execute(sql, human)
        await pool.commit()
        return cursor.lastrowid


async def update_human(pool, human):
    sql = ''' UPDATE humans
              SET public_key = %s, date_update = NOW() WHERE id = %s '''
    try:
        async with pool.cursor() as cursor:
            await cursor.execute(sql, human)
            await pool.commit()
            return cursor.rowcount, None

    except AttributeError as e:
        return 0, str(e)


async def delete_human(pool, human_id):
    sql = ''' DELETE FROM humans WHERE id = %s '''
    try:
        async with pool.cursor() as cursor:
            await cursor.execute(sql, human_id)
            await pool.commit()
            return cursor.rowcount, None

    except AttributeError as e:
        return 0, str(e)


async def get_humans(pool):
    sql = ''' SELECT id, public_key, face_encodings FROM humans '''
    async with pool.cursor() as cursor:
        await cursor.execute(sql)
        rows = await cursor.fetchall()
    return rows


async def check_human(pool, share_group):
    sql = '''
    SELECT shares.data, receiver FROM shares
    WHERE human_id = %s
    AND shared_id = %s;
    '''
    try:
        async with pool.cursor() as cursor:
            await cursor.execute(sql, (share_group['human_public_key'], share_group['share_public_key']))
            rows = await cursor.fetchall()
            return rows

    except Exception as e:
        return 0, str(e)
