import json

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse
from app.service.automations import AutomationService
from app.service.bible import BibleService
# from Typing import List, Dict, Any

router = APIRouter(prefix='/automations', tags=['Automations'])
automation_service = AutomationService()
bible_service = BibleService()


def make_pretty_response(content):
    return Response(
        content=json.dumps(content, indent=2),
        status_code=status.HTTP_200_OK,
        media_type="application/json"
    )


async def handle_exceptions(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


@router.get("/get_book_names", status_code=status.HTTP_200_OK)
async def get_book_names():
    try:
        book_names = {index: bible_service.get_book_names(index=index) for index in range(1, 67)}
        return make_pretty_response(book_names)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_book_structure", status_code=status.HTTP_200_OK)
async def get_book_structure(testament_name: str, book_number: int):
    try:
        structure = bible_service.get_book_structure(testament_name, book_number)
        if structure is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book not found for testament '{testament_name}' and book number {book_number}"
            )
        return make_pretty_response(structure)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/generate-questions-and-answers-for-verse", status_code=status.HTTP_200_OK)
async def generate_questions_and_answers_for_verse(
    request: Request,
    testament_name: str,
    book_number: int,
    chapter_number: int,
    start_verse_number: int,
    end_verse_number: int,
    number_of_questions: int = 1,
    level: str = "medium"
):
    try:
        response = automation_service.generate_questions_and_answers_for_verse(
            testament_name=testament_name,
            book_number=book_number,
            chapter_number=chapter_number,
            start_verse_number=start_verse_number,
            end_verse_number=end_verse_number,
            number_of_questions=number_of_questions,
            level=level
        )
        return make_pretty_response(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-questions-and-answers-for-chapter", status_code=status.HTTP_200_OK)
async def generate_questions_and_answers_for_chapter(
    request: Request,
    testament_name: str,
    book_number: int,
    chapter_number: int,
    number_of_questions: int = 1,
    level: str = "medium"
):
    try:
        response = automation_service.generate_questions_and_answers_for_chapter(
            testament_name=testament_name,
            book_number=book_number,
            chapter_number=chapter_number,
            number_of_questions=number_of_questions,
            level=level
        )
        return make_pretty_response(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-questions-and-answers-for-book", status_code=status.HTTP_200_OK)
async def generate_questions_and_answers_for_book(
    request: Request,
    testament_name: str,
    book_number: int,
    number_of_questions: int = 1,
    level: str = "medium"
):
    try:
        response = automation_service.generate_questions_and_answers_for_book(
            testament_name=testament_name,
            book_number=book_number,
            number_of_questions=number_of_questions,
            level=level
        )
        return make_pretty_response(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))