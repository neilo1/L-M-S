"""
Group A - Book Module
Purpose: Define the structure of a book.
Responsibilities: Store book data (ISBN, title, author, copies).
"""

class Book:
    """
    Represents a book in the library system.
    
    Attributes:
        isbn (str): The International Standard Book Number
        title (str): The title of the book
        author (str): The author of the book
        copies (int): Number of copies available
    """
    
    def __init__(self, isbn, title, author, copies):
        """
        Initialize a new Book instance.
        
        Args:
            isbn (str): The ISBN of the book
            title (str): The title of the book
            author (str): The author of the book
            copies (int): Number of copies available
        """
        self.isbn = isbn
        self.title = title
        self.author = author
        self.copies = copies
    
    def __str__(self):
        """
        Return string representation of the book.
        
        Returns:
            str: Formatted book information
        """
        return f"Book(ISBN: {self.isbn}, Title: '{self.title}', Author: '{self.author}', Copies: {self.copies})"
    
    def __repr__(self):
        """
        Return detailed string representation of the book.
        
        Returns:
            str: Detailed book information for debugging
        """
        return f"Book('{self.isbn}', '{self.title}', '{self.author}', {self.copies})"
    
    def is_available(self):
        """
        Check if the book is available for borrowing.
        
        Returns:
            bool: True if copies > 0, False otherwise
        """
        return self.copies > 0
    
    def get_info(self):
        """
        Get formatted book information.
        
        Returns:
            dict: Dictionary containing book information
        """
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'copies': self.copies,
            'available': self.is_available()
        }