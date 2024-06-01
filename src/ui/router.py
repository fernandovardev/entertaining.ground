from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Welcome to the Project", description="Displays a welcome message for the project.")
def welcome():
    return {"message": "Welcome to the Mage Grimoire Project!"}