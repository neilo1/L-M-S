"""
Group D - Issue and Return Module
Purpose: Handle book issuance and return.
Responsibilities: Update availability when members borrow or return books.
"""

def issue_book(library, isbn, member):
    """
    Issue a book to a member.
    
    Args:
        library (Library): Library instance
        isbn (str): ISBN of the book to issue
        member (Member): Member who wants to borrow the book
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Check if book exists
    book = library.get_book(isbn)
    if not book:
        return False, f"Book with ISBN {isbn} not found in library"
    
    # Check if book is available
    if book.copies <= 0:
        return False, f"Book '{book.title}' is not available (no copies left)"
    
    # Check if member already has this book
    if member.has_book(isbn):
        return False, f"Member {member.name} already has this book"
    
    # Issue the book
    book.copies -= 1
    member.borrow_book(isbn)
    
    return True, f"Book '{book.title}' issued to {member.name}"

def return_book(library, isbn, member):
    """
    Return a book from a member.
    
    Args:
        library (Library): Library instance
        isbn (str): ISBN of the book to return
        member (Member): Member who is returning the book
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Check if book exists
    book = library.get_book(isbn)
    if not book:
        return False, f"Book with ISBN {isbn} not found in library"
    
    # Check if member has this book
    if not member.has_book(isbn):
        return False, f"Member {member.name} doesn't have this book"
    
    # Return the book
    book.copies += 1
    member.return_book(isbn)
    
    return True, f"Book '{book.title}' returned by {member.name}"

def issue_book_by_id(library, isbn, member_id):
    """
    Issue a book to a member by member ID.
    
    Args:
        library (Library): Library instance
        isbn (str): ISBN of the book to issue
        member_id (str): ID of the member
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Get member
    member = library.get_member(member_id)
    if not member:
        return False, f"Member with ID {member_id} not found"
    
    return issue_book(library, isbn, member)

def return_book_by_id(library, isbn, member_id):
    """
    Return a book from a member by member ID.
    
    Args:
        library (Library): Library instance
        isbn (str): ISBN of the book to return
        member_id (str): ID of the member
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Get member
    member = library.get_member(member_id)
    if not member:
        return False, f"Member with ID {member_id} not found"
    
    return return_book(library, isbn, member)

def get_member_borrowed_books(library, member_id):
    """
    Get details of all books borrowed by a member.
    
    Args:
        library (Library): Library instance
        member_id (str): ID of the member
        
    Returns:
        tuple: (success: bool, data: list or message: str)
    """
    member = library.get_member(member_id)
    if not member:
        return False, f"Member with ID {member_id} not found"
    
    borrowed_details = []
    for isbn in member.borrowed_books:
        book = library.get_book(isbn)
        if book:
            borrowed_details.append({
                'isbn': isbn,
                'title': book.title,
                'author': book.author
            })
    
    return True, borrowed_details

def get_overdue_books(library):
    """
    Get list of all borrowed books (simplified - no date tracking in this version).
    
    Args:
        library (Library): Library instance
        
    Returns:
        list: List of borrowed book information
    """
    borrowed_books = []
    for member in library.list_members():
        for isbn in member.borrowed_books:
            book = library.get_book(isbn)
            if book:
                borrowed_books.append({
                    'member_id': member.member_id,
                    'member_name': member.name,
                    'isbn': isbn,
                    'title': book.title,
                    'author': book.author
                })
    
    return borrowed_books

def check_book_availability(library, isbn):
    """
    Check if a book is available for borrowing.
    
    Args:
        library (Library): Library instance
        isbn (str): ISBN of the book to check
        
    Returns:
        tuple: (exists: bool, available: bool, copies: int, message: str)
    """
    book = library.get_book(isbn)
    if not book:
        return False, False, 0, f"Book with ISBN {isbn} not found"
    
    available = book.copies > 0
    message = f"Book '{book.title}' - {book.copies} copies available" if available else f"Book '{book.title}' - No copies available"
    
    return True, available, book.copies, message