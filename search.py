"""
Group E - Search Module
Purpose: Enable search by title, author, or ISBN.
Responsibilities: Help users find available books.
"""

def search_by_title(library, title):
    """
    Search for books by title (case-insensitive partial match).
    
    Args:
        library (Library): Library instance
        title (str): Title to search for
        
    Returns:
        list: List of Book objects matching the title
    """
    if not title:
        return []
    
    title_lower = title.lower()
    matching_books = []
    
    for book in library.books.values():
        if title_lower in book.title.lower():
            matching_books.append(book)
    
    return matching_books

def search_by_author(library, author):
    """
    Search for books by author (case-insensitive partial match).
    
    Args:
        library (Library): Library instance
        author (str): Author name to search for
        
    Returns:
        list: List of Book objects by the author
    """
    if not author:
        return []
    
    author_lower = author.lower()
    matching_books = []
    
    for book in library.books.values():
        if author_lower in book.author.lower():
            matching_books.append(book)
    
    return matching_books

def search_by_isbn(library, isbn):
    """
    Search for a book by exact ISBN.
    
    Args:
        library (Library): Library instance
        isbn (str): ISBN to search for
        
    Returns:
        Book or None: Book object if found, None otherwise
    """
    return library.get_book(isbn)

def search_books(library, query, search_type="all"):
    """
    General search function that searches by title, author, or ISBN.
    
    Args:
        library (Library): Library instance
        query (str): Search query
        search_type (str): Type of search - "title", "author", "isbn", or "all"
        
    Returns:
        list: List of Book objects matching the query
    """
    if not query:
        return []
    
    results = []
    
    if search_type in ["all", "title"]:
        results.extend(search_by_title(library, query))
    
    if search_type in ["all", "author"]:
        author_results = search_by_author(library, query)
        # Avoid duplicates
        for book in author_results:
            if book not in results:
                results.append(book)
    
    if search_type in ["all", "isbn"]:
        isbn_result = search_by_isbn(library, query)
        if isbn_result and isbn_result not in results:
            results.append(isbn_result)
    
    return results

def search_available_books(library, query, search_type="all"):
    """
    Search for books that are currently available for borrowing.
    
    Args:
        library (Library): Library instance
        query (str): Search query
        search_type (str): Type of search - "title", "author", "isbn", or "all"
        
    Returns:
        list: List of available Book objects matching the query
    """
    all_results = search_books(library, query, search_type)
    return [book for book in all_results if book.copies > 0]

def advanced_search(library, title=None, author=None, isbn=None, available_only=False):
    """
    Advanced search with multiple criteria.
    
    Args:
        library (Library): Library instance
        title (str, optional): Title to search for
        author (str, optional): Author to search for
        isbn (str, optional): ISBN to search for
        available_only (bool): If True, only return available books
        
    Returns:
        list: List of Book objects matching all criteria
    """
    results = list(library.books.values())
    
    # Filter by title if provided
    if title:
        title_lower = title.lower()
        results = [book for book in results if title_lower in book.title.lower()]
    
    # Filter by author if provided
    if author:
        author_lower = author.lower()
        results = [book for book in results if author_lower in book.author.lower()]
    
    # Filter by ISBN if provided
    if isbn:
        results = [book for book in results if book.isbn == isbn]
    
    # Filter by availability if requested
    if available_only:
        results = [book for book in results if book.copies > 0]
    
    return results

def get_search_suggestions(library, partial_query, max_suggestions=5):
    """
    Get search suggestions based on partial query.
    
    Args:
        library (Library): Library instance
        partial_query (str): Partial search query
        max_suggestions (int): Maximum number of suggestions to return
        
    Returns:
        dict: Dictionary with title and author suggestions
    """
    if not partial_query or len(partial_query) < 2:
        return {'titles': [], 'authors': []}
    
    query_lower = partial_query.lower()
    title_suggestions = set()
    author_suggestions = set()
    
    for book in library.books.values():
        # Title suggestions
        if query_lower in book.title.lower():
            title_suggestions.add(book.title)
        
        # Author suggestions
        if query_lower in book.author.lower():
            author_suggestions.add(book.author)
        
        # Stop if we have enough suggestions
        if len(title_suggestions) >= max_suggestions and len(author_suggestions) >= max_suggestions:
            break
    
    return {
        'titles': list(title_suggestions)[:max_suggestions],
        'authors': list(author_suggestions)[:max_suggestions]
    }

def search_statistics(library, query):
    """
    Get statistics about search results.
    
    Args:
        library (Library): Library instance
        query (str): Search query
        
    Returns:
        dict: Dictionary with search statistics
    """
    all_results = search_books(library, query)
    available_results = search_available_books(library, query)
    
    return {
        'total_matches': len(all_results),
        'available_matches': len(available_results),
        'unavailable_matches': len(all_results) - len(available_results),
        'query': query
    }