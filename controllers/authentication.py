from fastapi import APIRouter, status

from models import Face, Human

from database import db_connect, db_shutdown
from database.humans import create_human, get_humans

from services.token import create_access_token
from services.store import add_human, get_face_encodings, get_human

from services.face_identification import get_encodings_from_image, get_identification, get_encodings_from_string, check_face_equality


authentication_controller: APIRouter = APIRouter(tags=["Authentication"])


# 1. identification 2. if (face exists in db) return data || redirect to settings data
@authentication_controller.post("/identification", status_code=status.HTTP_200_OK)
async def identification(face_data: Face):
    print('Identification Procces')
    try:
        # DB Connection
        pool = await db_connect()
        # From Base64 to Face_encodings
        unknown_encoding = get_encodings_from_image(face_data)
        # Get People Faces
        rows = await get_humans(pool)
        # Identify Face in Rows
        person = get_identification(rows, unknown_encoding)
        if person:
            # Create Access Token
            access_token = create_access_token(person['id'])
            # Check Human's public key again
            stored_face_encodings = await get_face_encodings(person['public_key'])
            if (stored_face_encodings):
                if (check_face_equality(stored_face_encodings['face_encodings'], person['face_encodings'])):
                    new_person = await get_human(person['public_key'])
                    return {"face": face_data, "person": new_person, "access_token": access_token}
                else:
                    return {"status": "error", "message": "Face is not the same as the original"}
            else:
                return {"status": "error", "message": "No Face in Data Store."}
        else:
            # Redirect to settings
            new_encodings = str(unknown_encoding.tolist())
            return {"face": face_data, "face_encodings": new_encodings}

    except Exception as e:
        print(e)
        await db_shutdown()
        return {"status": "error", "message": "Unable to Identify."}


@authentication_controller.post("/registration", status_code=status.HTTP_200_OK)
async def registration(human_data: Human):
    print('Registration Procces')
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
            return {"status": "error", "message": "You already exist in the system!"}
        else:
            formated_encodings = str(human_data.face_encodings)
            person = (human_data.public_key, formated_encodings)
            person_id = await create_human(pool, person)
            create_person = (
                {
                    "id": person_id,
                    "public_key": human_data.public_key,
                    "face_encodings": formated_encodings,
                    "encrypted_public_key": human_data.encrypted_public_key,
                    "encrypted_private_key": human_data.encrypted_private_key
                }
            )
            # Add Human to SmartContract
            add_transaction = await add_human(human_data)
            access_token = create_access_token(person_id)
            return {"person": create_person, "access_token": access_token}

    except Exception as e:
        print(e)
        await db_shutdown()
        return {"status": "error", "message": "Unable to Register Data."}
