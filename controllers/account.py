from fastapi import APIRouter, Depends, status

from models import Face, Human, Share, Ban

from database import db_connect, db_shutdown
from database.humans import create_human, get_humans, update_human, delete_human, check_human
from database.share import create_share, get_access, update_share, delete_share, get_shares, get_accesses

from services.token import create_access_token, decode_access_token, identify_user
from services.store import add_human, kill_human, get_face_encodings, get_human, refresh_human

from services.face_identification import get_encodings_from_image, get_identification, get_encodings_from_string, check_face_equality


account_controller: APIRouter = APIRouter(tags=["Account"])


@account_controller.post("/profile", status_code=status.HTTP_201_CREATED)
async def profile():
    return 0


@account_controller.post("/update", status_code=status.HTTP_200_OK)
async def update(human_data: Human, current_user: int = Depends(identify_user)):
    print('Update Procces')
    try:
        # DB Connection
        pool = await db_connect()
        # Get People Faces
        rows = await get_humans(pool)
        # Get Face from Str
        unknown_encoding = get_encodings_from_string(human_data.face_encodings)
        # Identify Face in Rows
        person = get_identification(rows, unknown_encoding)
        if person:
            formated_encodings = str(human_data.face_encodings)
            old_public_key = person['public_key']
            person = (human_data.public_key, current_user)
            update_status = await update_human(pool, person)
            updated_human = (
                {
                    "id": current_user,
                    "public_key": human_data.public_key,
                    "face_encodings": formated_encodings,
                    "encrypted_public_key": human_data.encrypted_public_key,
                    "encrypted_private_key": human_data.encrypted_private_key,
                }
            )
            # Update Human in SmartContract
            update_transaction = await refresh_human(old_public_key, human_data)
            access_token = create_access_token(current_user)
            return {"person": updated_human, "access_token": access_token}
        else:
            return {"status": "error", "message": "You are not in the system."}

    except Exception as e:
        print(e)
        await db_shutdown()
        return {"status": "error", "message": "Unable to Update Data."}


@account_controller.post("/delete", status_code=status.HTTP_200_OK)
async def delete(human_data: Human, current_user: int = Depends(identify_user)):
    print('Delete Procces')
    try:
        # DB Connection
        pool = await db_connect()
        # Get People Faces
        rows = await get_humans(pool)
        # Get Face from Str
        unknown_encoding = get_encodings_from_string(human_data.face_encodings)
        # Identify Face in Rows
        person = get_identification(rows, unknown_encoding)
        if person:
            formated_encodings = str(human_data.face_encodings)
            delete_status = await delete_human(pool, current_user)
            deleted_human = (
                {
                    "id": current_user,
                    "public_key": human_data.public_key,
                    "face_encodings": formated_encodings
                }
            )
            # Kill Human in SmartContract
            killed_transaction = await kill_human(human_data)
            return {"status": "success", "message": "Data erased successfully."}
        else:
            return {"status": "error", "message": "You are not in the system."}

    except Exception as e:
        print(e)
        await db_shutdown()
        return {"status": "error", "message": "Unable to Delete Data."}


@account_controller.get("/id/{human_public_key}/{share_public_key}", status_code=status.HTTP_200_OK)
async def check_access(human_public_key: str, share_public_key: str, current_user: int = Depends(identify_user)):
    print('Check Access Procces')
    try:
        # DB Connection
        pool = await db_connect()
        share_group = {
            'human_public_key': human_public_key,
            'share_public_key': share_public_key
        }
        get_status = await check_human(pool, share_group)
        person = await get_human(share_public_key)

        if get_status != None:
            return {"status": "success", "data": get_status, "encrypted_public_key": person['encrypted_public_key']}
        else:
            return {"status": "error", "message": "Error in getting Data."}

    except Exception as e:
        print(e)
        await db_shutdown()
        return {"status": "error", "message": "Unable to Get Data."}


# Users whom i gave access
@account_controller.get("/shares/{human_public_key}", status_code=status.HTTP_200_OK)
async def get_all_shares(human_public_key: str, current_user: int = Depends(identify_user)):
    print('Shares List Procces')
    try:
        # DB Connection
        pool = await db_connect()

        shares = await get_shares(pool, human_public_key)

        return {"shares": shares}

    except Exception as e:
        print(e)
        await db_shutdown()
        return {"status": "error", "message": "Unable to Get Data."}


# Users whom  gave me access
@account_controller.get("/accesses/{human_public_key}", status_code=status.HTTP_200_OK)
async def get_all_accesses(human_public_key: str, current_user: int = Depends(identify_user)):
    print('Acceses List Procces')
    try:
        # DB Connection
        pool = await db_connect()

        accesses = await get_accesses(pool, human_public_key)

        return {"accesses": accesses}

    except Exception as e:
        print(e)
        await db_shutdown()
        return {"status": "error", "message": "Unable to Get Data."}


@account_controller.post("/share", status_code=status.HTTP_200_OK)
async def share(share_data: Share, current_user: int = Depends(identify_user)):
    print('Share Procces')
    try:
        # DB Connection
        pool = await db_connect()
        new_share = (
            share_data.human_id,
            share_data.shared_id,
            share_data.receiver,
            share_data.data
        )
        share = await create_share(pool, new_share)

        access_token = create_access_token(current_user)
        return {"share": share, "access_token": access_token}

    except Exception as e:
        print(e)
        await db_shutdown()
        return {"status": "error", "message": "Unable to Register Data."}


@account_controller.post("/ban", status_code=status.HTTP_200_OK)
async def ban(share_data: Ban, current_user: int = Depends(identify_user)):
    print('Ban Procces')
    try:
        # DB Connection
        pool = await db_connect()
        new_share = (share_data.human_id, share_data.shared_id)
        share = await delete_share(pool, new_share)

        access_token = create_access_token(current_user)
        return {"share": share, "access_token": access_token}

    except Exception as e:
        print(e)
        await db_shutdown()
        return {"status": "error", "message": "Unable to Ban."}


@account_controller.post("/renew", status_code=status.HTTP_200_OK)
async def renew(share_data: Share, current_user: int = Depends(identify_user)):
    print('Share Procces')
    try:
        # DB Connection
        pool = await db_connect()
        new_share = (
            share_data.data,
            share_data.receiver,
            share_data.human_id,
            share_data.shared_id,
        )
        share = await update_share(pool, new_share)

        access_token = create_access_token(current_user)
        return {"share": share, "access_token": access_token}

    except Exception as e:
        print(e)
        await db_shutdown()
        return {"status": "error", "message": "Unable to Register Data."}


@account_controller.get("/access/{human_public_key}/{share_public_key}", status_code=status.HTTP_200_OK)
async def check_access(human_public_key: str, share_public_key: str, current_user: int = Depends(identify_user)):
    print('Get Access Procces')
    try:
        # DB Connection
        pool = await db_connect()
        share_group = {
            'human_public_key': human_public_key,
            'share_public_key': share_public_key
        }
        get_status = await get_access(pool, share_group)
        print(get_status)

        if get_status != None:
            return {"status": "success", "data": get_status}
        else:
            return {"status": "error", "message": "Error in getting Data."}

    except Exception as e:
        print(e)
        await db_shutdown()
        return {"status": "error", "message": "Unable to Get Data."}
