import json


class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author


class BookPages:
    def __init__(self):
        self.current_page = 1

    def turn_page(self):
        self.current_page += 1
        print(f'Page turned. Current page is {self.current_page}')

    def get_current_page(self):
        return f"Page {self.current_page} content"


class BookLocation:
    def __init__(self, shelf_number: int, room_number: int):
        self.shelf_number = shelf_number
        self.room_number = room_number

    def get_location(self):
        return f"Shelf: {self.shelf_number}, Room: {self.room_number}"


class BookSaver:
    def save(self, book_info: Book, page_navigator: BookPages):
        filename = f'.\\Outputs\\{book_info.get_title()}-{book_info.get_author()}.json'
        data = {
            'title': book_info.get_title(),
            'author': book_info.get_author(),
            'current_page': page_navigator.get_current_page()
        }
        with open(filename, 'w') as file:
            json.dump(data, file)


class Printer:
    def print_page(page):
        print(page)


class PlainTextPrinter(Printer):
    def print_text(self, page):
        Printer.print_page(page)


class HtmlPrinter(Printer):
    def print_html(self, page):
        Printer.print_page(page)


if __name__ == "__main__":
    book_info = Book("A Great Book", "John Doe")
    book_page = BookPages()

    book_page.turn_page()
    book_page.turn_page()

    printer = PlainTextPrinter()
    page = book_page.get_current_page()
    printer.print_text(page)

    book_saver = BookSaver()
    book_saver.save(book_info, book_page)

    book_location = BookLocation(5, 2)
    print(book_location.get_location())
