from lxml import etree

# tree = etree.parse("source/EnglishNIVBible.xml")


# root = tree.getroot()




# print(verse.text)

# old_testament = root.find("testament")
# book = old_testament.find("book")
# chapter = book.find("chapter")
# verse = chapter.find("verse")

# print(verse.text)

# print("Root element:", root.tag)

# for child in root:
#     print("Tag:", child.tag)
#     print("Text:", child.text)


class BibleService:
    def __init__(self, xml_file = "source/EnglishNIVBible.xml"):
        self.tree = etree.parse(xml_file)
        self.root = self.tree.getroot()

    
    def get_book_names(self, **kwargs):
        bible_books = {
            1: "Genesis",
            2: "Exodus",
            3: "Leviticus",
            4: "Numbers",
            5: "Deuteronomy",
            6: "Joshua",
            7: "Judges",
            8: "Ruth",
            9: "1 Samuel",
            10: "2 Samuel",
            11: "1 Kings",
            12: "2 Kings",
            13: "1 Chronicles",
            14: "2 Chronicles",
            15: "Ezra",
            16: "Nehemiah",
            17: "Esther",
            18: "Job",
            19: "Psalms",
            20: "Proverbs",
            21: "Ecclesiastes",
            22: "Song of Solomon",
            23: "Isaiah",
            24: "Jeremiah",
            25: "Lamentations",
            26: "Ezekiel",
            27: "Daniel",
            28: "Hosea",
            29: "Joel",
            30: "Amos",
            31: "Obadiah",
            32: "Jonah",
            33: "Micah",
            34: "Nahum",
            35: "Habakkuk",
            36: "Zephaniah",
            37: "Haggai",
            38: "Zechariah",
            39: "Malachi",
            40: "Matthew",
            41: "Mark",
            42: "Luke",
            43: "John",
            44: "Acts",
            45: "Romans",
            46: "1 Corinthians",
            47: "2 Corinthians",
            48: "Galatians",
            49: "Ephesians",
            50: "Philippians",
            51: "Colossians",
            52: "1 Thessalonians",
            53: "2 Thessalonians",
            54: "1 Timothy",
            55: "2 Timothy",
            56: "Titus",
            57: "Philemon",
            58: "Hebrews",
            59: "James",
            60: "1 Peter",
            61: "2 Peter",
            62: "1 John",
            63: "2 John",
            64: "3 John",
            65: "Jude",
            66: "Revelation"
        }

        get_book_name = bible_books.get(kwargs.get("index"), "Unknown Book")
        return get_book_name

    def get_verse(self, testament_name, book_number, chapter_number, verse_number):
        xpath = (
            f"./testament[@name='{testament_name}']"
            f"/book[@number='{book_number}']"
            f"/chapter[@number='{chapter_number}']"
            f"/verse[@number='{verse_number}']"
        )

        verse = self.root.find(xpath)

        return verse.text if verse is not None else None
    
    def get_range_of_verses(self, testament_name, book_number, chapter_number, start_verse_number, end_verse_number):
        verses = []
        for verse_number in range(start_verse_number, end_verse_number + 1):
            verse_text = self.get_verse(testament_name, book_number, chapter_number, verse_number)
            if verse_text is not None:
                verses.append(verse_text)
        return verses
    
    def get_chapter(self, testament_name, book_number, chapter_number):
        xpath = (
            f"./testament[@name='{testament_name}']"
            f"/book[@number='{book_number}']"
            f"/chapter[@number='{chapter_number}']"
        )

        chapter = self.root.find(xpath)

        if chapter is not None:
            verses = [verse.text for verse in chapter.findall("verse")]
            return verses
        else:
            return None
        
    def get_book(self, testament_name, book_number):
        xpath = (
            f"./testament[@name='{testament_name}']"
            f"/book[@number='{book_number}']"
        )

        book = self.root.find(xpath)

        if book is not None:
            chapters = {}
            for chapter in book.findall("chapter"):
                chapter_number = int(chapter.get("number"))
                verses = [verse.text for verse in chapter.findall("verse")]
                chapters[chapter_number] = verses
            return chapters
        else:
            return None
        



# get_verse = BibleService().get_verse("Old", 1, 1, 1)
# get_range_of_verses = BibleService().get_range_of_verses("Old", 1, 1, 1, 3)
# # get_chapter = BibleService().get_chapter("Old", 1, 1)
# # get_book = BibleService().get_book("Old", 1)

# # print("Single Verse:", get_verse)
# print("Range of Verses:", get_range_of_verses)
# # print("Chapter:", get_chapter)
# # print("Book:", get_book)


bible_service = BibleService()
