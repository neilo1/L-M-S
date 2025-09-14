"""
Group B - Member Module
Purpose: Manage library members.
Responsibilities: Track member ID, name, and borrowed books.
"""

class Member:
    """
    Represents a library member.
    
    Attributes:
        member_id (str): Unique identifier for the member
        name (str): Name of the member
        borrowed_books (list): List of ISBNs of borrowed books
    """
    
    def __init__(self, member_id, name):
        """
        Initialize a new Member instance.
        
        Args:
            member_id (str): Unique identifier for the member
            name (str): Name of the member
        """
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []
    
    def __str__(self):
        """
        Return string representation of the member.
        
        Returns:
            str: Formatted member information
        """
        return f"Member(ID: {self.member_id}, Name: '{self.name}', Books: {len(self.borrowed_books)})"
    
    def __repr__(self):
        """
        Return detailed string representation of the member.
        
        Returns:
            str: Detailed member information for debugging
        """
        return f"Member('{self.member_id}', '{self.name}')"
    
    def borrow_book(self, isbn):
        """
        Add a book to the member's borrowed books list.
        
        Args:
            isbn (str): ISBN of the book to borrow
            
        Returns:
            bool: True if book was added successfully
        """
        if isbn not in self.borrowed_books:
            self.borrowed_books.append(isbn)
            return True
        return False
    
    def return_book(self, isbn):
        """
        Remove a book from the member's borrowed books list.
        
        Args:
            isbn (str): ISBN of the book to return
            
        Returns:
            bool: True if book was removed successfully, False if not found
        """
        if isbn in self.borrowed_books:
            self.borrowed_books.remove(isbn)
            return True
        return False
    
    def has_book(self, isbn):
        """
        Check if member has borrowed a specific book.
        
        Args:
            isbn (str): ISBN of the book to check
            
        Returns:
            bool: True if member has the book, False otherwise
        """
        return isbn in self.borrowed_books
    
    def get_borrowed_count(self):
        """
        Get the number of books currently borrowed.
        
        Returns:
            int: Number of borrowed books
        """
        return len(self.borrowed_books)
    
    def get_info(self):
        """
        Get formatted member information.
        
        Returns:
            dict: Dictionary containing member information
        """
        return {
            'member_id': self.member_id,
            'name': self.name,
            'borrowed_books': self.borrowed_books.copy(),
            'books_count': len(self.borrowed_books)
        }