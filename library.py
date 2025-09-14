"""
Group C - Library Module
Purpose: Manage library's book collection.
Responsibilities: Add, remove, and list books.
"""

class Library:
    """
    Represents the library system that manages books and members.
    
    Attributes:
        books (dict): Dictionary of books with ISBN as key
        members (dict): Dictionary of members with member_id as key
    """
    
    def __init__(self):
        """
        Initialize a new Library instance.
        """
        self.books = {}
        self.members = {}
    
    def add_book(self, book):
        """
        Add a book to the library collection.
        
        Args:
            book (Book): Book object to add to the library
            
        Returns:
            bool: True if book was added successfully
        """
        self.books[book.isbn] = book
        return True
    
    def remove_book(self, isbn):
        """
        Remove a book from the library collection.
        
        Args:
            isbn (str): ISBN of the book to remove
            
        Returns:
            bool: True if book was removed, False if not found
        """
        if isbn in self.books:
            del self.books[isbn]
            return True
        return False
    
    def get_book(self, isbn):
        """
        Get a book by its ISBN.
        
        Args:
            isbn (str): ISBN of the book to retrieve
            
        Returns:
            Book: Book object if found, None otherwise
        """
        return self.books.get(isbn)
    
    def add_member(self, member):
        """
        Add a member to the library system.
        
        Args:
            member (Member): Member object to add
            
        Returns:
            bool: True if member was added successfully
        """
        self.members[member.member_id] = member
        return True
    
    def remove_member(self, member_id):
        """
        Remove a member from the library system.
        
        Args:
            member_id (str): ID of the member to remove
            
        Returns:
            bool: True if member was removed, False if not found
        """
        if member_id in self.members:
            del self.members[member_id]
            return True
        return False
    
    def get_member(self, member_id):
        """
        Get a member by their ID.
        
        Args:
            member_id (str): ID of the member to retrieve
            
        Returns:
            Member: Member object if found, None otherwise
        """
        return self.members.get(member_id)
    
    def list_books(self):
        """
        Get a list of all books in the library.
        
        Returns:
            list: List of Book objects
        """
        return list(self.books.values())
    
    def list_members(self):
        """
        Get a list of all members in the library.
        
        Returns:
            list: List of Member objects
        """
        return list(self.members.values())
    
    def get_available_books(self):
        """
        Get a list of books that are available for borrowing.
        
        Returns:
            list: List of Book objects with copies > 0
        """
        return [book for book in self.books.values() if book.copies > 0]
    
    def get_library_stats(self):
        """
        Get library statistics.
        
        Returns:
            dict: Dictionary containing library statistics
        """
        total_books = len(self.books)
        available_books = len(self.get_available_books())
        total_members = len(self.members)
        total_borrowed = sum(len(member.borrowed_books) for member in self.members.values())
        
        return {
            'total_books': total_books,
            'available_books': available_books,
            'total_members': total_members,
            'books_borrowed': total_borrowed
        }