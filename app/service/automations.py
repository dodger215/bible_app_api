import json
import re

from app.service.bible import BibleService
from app.service.chatbot import generate_response


class AutomationService:
    def __init__(self):
        self.bible_service = BibleService()

    def normalize_scripture_text(self, text):
        if isinstance(text, list):
            return "\n".join(text)
        if isinstance(text, dict):
            return json.dumps(text, indent=2)
        return str(text)

    def prompt(self, **kwargs):
        text = self.normalize_scripture_text(kwargs.get("text", ""))
        number = kwargs.get("number", 1)

        prompt = f"""You are a Bible study assistant. Based on the scripture passage provided below, generate exactly {number} unique questions and their corresponding answers.

Scripture:
{text}

Instructions:
- Questions should be directly derived from the scripture.
- Avoid duplicate or overly similar questions.
- Include a mix of recall, comprehension, and application questions when appropriate.
- Answers must be accurate, concise, and based solely on the provided scripture.
- Return only valid JSON without any additional text, explanations, or markdown.
- Do not wrap the JSON in markdown code fences.

Expected JSON format:

{{
  "questions": [
    {{
      "index": 1,
      "question": "Who spoke to Moses?",
      "answer": "God spoke to Moses."
    }}
  ]
}}"""
        return prompt

    def parse_response(self, response_text):
        if isinstance(response_text, dict):
            payload = response_text
        else:
            raw = str(response_text).strip()
            raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.IGNORECASE)
            raw = re.sub(r"\s*```$", "", raw, flags=re.IGNORECASE)
            if raw.startswith('"') and raw.endswith('"'):
                raw = raw[1:-1]

            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                match = re.search(r"(\{.*\})", raw, flags=re.DOTALL)
                if not match:
                    raise
                payload = json.loads(match.group(1))

        if not isinstance(payload, dict):
            raise ValueError("Model response is not a JSON object.")

        questions = payload.get("questions")
        if isinstance(questions, list):
            normalized = []
            for index, item in enumerate(questions, start=1):
                if isinstance(item, dict):
                    item.setdefault("index", index)
                    normalized.append(item)
            payload["questions"] = normalized

        return payload

    def generate_questions_and_answers_for_verse(self, **kwargs):
        testament_name = kwargs.get("testament_name")
        book_number = kwargs.get("book_number")
        chapter_number = kwargs.get("chapter_number")
        start_verse_number = kwargs.get("start_verse_number")
        end_verse_number = kwargs.get("end_verse_number")
        number_of_questions = kwargs.get("number_of_questions", 1)

        verse_text = self.bible_service.get_range_of_verses(
            testament_name, book_number, chapter_number, start_verse_number, end_verse_number
        )

        if verse_text is None:
            return {"error": "Verse not found."}

        prompt = self.prompt(text=verse_text, number=number_of_questions)
        response = generate_response(prompt)
        return self.parse_response(response)

    def generate_questions_and_answers_for_chapter(self, **kwargs):
        testament_name = kwargs.get("testament_name")
        book_number = kwargs.get("book_number")
        chapter_number = kwargs.get("chapter_number")
        number_of_questions = kwargs.get("number_of_questions", 1)

        chapter_text = self.bible_service.get_chapter(
            testament_name, book_number, chapter_number
        )

        if chapter_text is None:
            return {"error": "Chapter not found."}

        prompt = self.prompt(text=chapter_text, number=number_of_questions)
        response = generate_response(prompt)
        return self.parse_response(response)

    def generate_questions_and_answers_for_book(self, **kwargs):
        testament_name = kwargs.get("testament_name")
        book_number = kwargs.get("book_number")
        number_of_questions = kwargs.get("number_of_questions", 1)

        book_text = self.bible_service.get_book(testament_name, book_number)

        if book_text is None:
            return {"error": "Book not found."}

        prompt = self.prompt(text=book_text, number=number_of_questions)
        response = generate_response(prompt)
        return self.parse_response(response)