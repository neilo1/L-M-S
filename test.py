"""
Group H - Unit Testing Module
Purpose: Ensure modules work correctly.
Responsibilities: Write tests for all major functions.
"""

import unittest
from book import Book
from member import Member
from library import Library
from issue_return import (
    issue_book, return_book, issue_book_by_id, return_book_by_id,
    get_member_borrowed_books, check_book_availability
)
from search import (
    search_by_title, search_by_author, search_by_isbn, search_books,
    search_available_books, advanced_search
)
from auth_system import AuthSystem, authenticate

class TestBook(unittest.TestCase):
    """Test cases for the Book class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.book = Book("978-0134685991", "Effective Java", "Joshua Bloch", 3)
    
    def test_book_creation(self):
        """Test book creation with valid data."""
        self.assertEqual(self.book.isbn, "978-0134685991")
        self.assertEqual(self.book.title, "Effective Java")
        self.assertEqual(self.book.author, "Joshua Bloch")
        self.assertEqual(self.book.copies, 3)
    
    def test_book_str_representation(self):
        """Test string representation of book."""
        expected = "Book(ISBN: 978-0134685991, Title: 'Effective Java', Author: 'Joshua Bloch', Copies: 3)"
        self.assertEqual(str(self.book), expected)
    
    def test_book_availability(self):
        """Test book availability check."""
        self.assertTrue(self.book.is_available())
        
        # Set copies to 0
        self.book.copies = 0
        self.assertFalse(self.book.is_available())
    
    def test_get_info(self):
        """Test get_info method."""
        info = self.book.get_info()
        self.assertEqual(info['isbn'], "978-0134685991")
        self.assertEqual(info['title'], "Effective Java")
        self.assertEqual(info['author'], "Joshua Bloch")
        self.assertEqual(info['copies'], 3)
        self.assertTrue(info['available'])

class TestMember(unittest.TestCase):
    """Test cases for the Member class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.member = Member("M001", "Alice Johnson")
    
    def test_member_creation(self):
        """Test member creation with valid data."""
        self.assertEqual(self.member.member_id, "M001")
        self.assertEqual(self.member.name, "Alice Johnson")
        self.assertEqual(self.member.borrowed_books, [])
    
    def test_borrow_book(self):
        """Test borrowing a book."""
        isbn = "978-0134685991"
        result = self.member.borrow_book(isbn)
        
        self.assertTrue(result)
        self.assertIn(isbn, self.member.borrowed_books)
        self.assertEqual(len(self.member.borrowed_books), 1)
    
    def test_borrow_duplicate_book(self):
        """Test borrowing the same book twice."""
        isbn = "978-0134685991"
        self.member.borrow_book(isbn)
        result = self.member.borrow_book(isbn)  # Try to borrow again
        
        self.assertFalse(result)
        self.assertEqual(len(self.member.borrowed_books), 1)
    
    def test_return_book(self):
        """Test returning a book."""
        isbn = "978-0134685991"
        self.member.borrow_book(isbn)
        result = self.member.return_book(isbn)
        
        self.assertTrue(result)
        self.assertNotIn(isbn, self.member.borrowed_books)
        self.assertEqual(len(self.member.borrowed_books), 0)
    
    def test_return_non_borrowed_book(self):
        """Test returning a book that wasn't borrowed."""
        isbn = "978-0134685991"
        result = self.member.return_book(isbn)
        
        self.assertFalse(result)
    
    def test_has_book(self):
        """Test checking if member has a specific book."""
        isbn = "978-0134685991"
        self.assertFalse(self.member.has_book(isbn))
        
        self.member.borrow_book(isbn)
        self.assertTrue(self.member.has_book(isbn))

class TestLibrary(unittest.TestCase):
    """Test cases for the Library class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.library = Library()
        self.book = Book("978-0134685991", "Effective Java", "Joshua Bloch", 3)
        self.member = Member("M001", "Alice Johnson")
    
    def test_add_book(self):
        """Test adding a book to the library."""
        result = self.library.add_book(self.book)
        
        self.assertTrue(result)
        self.assertIn(self.book.isbn, self.library.books)
        self.assertEqual(self.library.books[self.book.isbn], self.book)
    
    def test_get_book(self):
        """Test getting a book by ISBN."""
        self.library.add_book(self.book)
        retrieved_book = self.library.get_book(self.book.isbn)
        
        self.assertEqual(retrieved_book, self.book)
    
    def test_get_nonexistent_book(self):
        """Test getting a book that doesn't exist."""
        retrieved_book = self.library.get_book("nonexistent")
        
        self.assertIsNone(retrieved_book)
    
    def test_remove_book(self):
        """Test removing a book from the library."""
        self.library.add_book(self.book)
        result = self.library.remove_book(self.book.isbn)
        
        self.assertTrue(result)
        self.assertNotIn(self.book.isbn, self.library.books)
    
    def test_remove_nonexistent_book(self):
        """Test removing a book that doesn't exist."""
        result = self.library.remove_book("nonexistent")
        
        self.assertFalse(result)
    
    def test_add_member(self):
        """Test adding a member to the library."""
        result = self.library.add_member(self.member)
        
        self.assertTrue(result)
        self.assertIn(self.member.member_id, self.library.members)
    
    def test_get_available_books(self):
        """Test getting available books."""
        book1 = Book("123", "Book 1", "Author 1", 2)
        book2 = Book("456", "Book 2", "Author 2", 0)  # No copies
        
        self.library.add_book(book1)
        self.library.add_book(book2)
        
        available_books = self.library.get_available_books()
        
        self.assertEqual(len(available_books), 1)
        self.assertIn(book1, available_books)
        self.assertNotIn(book2, available_books)

class TestIssueReturn(unittest.TestCase):
    """Test cases for issue and return functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.library = Library()
        self.book = Book("978-0134685991", "Effective Java", "Joshua Bloch", 3)
        self.member = Member("M001", "Alice Johnson")
        
        self.library.add_book(self.book)
        self.library.add_member(self.member)
    
    def test_issue_book_success(self):
        """Test successful book issuance."""
        success, message = issue_book(self.library, self.book.isbn, self.member)
        
        self.assertTrue(success)
        self.assertIn("issued", message.lower())
        self.assertEqual(self.book.copies, 2)  # Decreased by 1
        self.assertIn(self.book.isbn, self.member.borrowed_books)
    
    def test_issue_nonexistent_book(self):
        """Test issuing a book that doesn't exist."""
        success, message = issue_book(self.library, "nonexistent", self.member)
        
        self.assertFalse(success)
        self.assertIn("not found", message.lower())
    
    def test_issue_unavailable_book(self):
        """Test issuing a book with no copies."""
        self.book.copies = 0
        success, message = issue_book(self.library, self.book.isbn, self.member)
        
        self.assertFalse(success)
        self.assertIn("not available", message.lower())
    
    def test_issue_duplicate_book(self):
        """Test issuing a book already borrowed by member."""
        # First issue
        issue_book(self.library, self.book.isbn, self.member)
        
        # Try to issue again
        success, message = issue_book(self.library, self.book.isbn, self.member)
        
        self.assertFalse(success)
        self.assertIn("already has", message.lower())
    
    def test_return_book_success(self):
        """Test successful book return."""
        # First issue the book
        issue_book(self.library, self.book.isbn, self.member)
        original_copies = self.book.copies
        
        # Then return it
        success, message = return_book(self.library, self.book.isbn, self.member)
        
        self.assertTrue(success)
        self.assertIn("returned", message.lower())
        self.assertEqual(self.book.copies, original_copies + 1)
        self.assertNotIn(self.book.isbn, self.member.borrowed_books)
    
    def test_return_non_borrowed_book(self):
        """Test returning a book not borrowed by member."""
        success, message = return_book(self.library, self.book.isbn, self.member)
        
        self.assertFalse(success)
        self.assertIn("doesn't have", message.lower())
    
    def test_check_book_availability(self):
        """Test checking book availability."""
        exists, available, copies, message = check_book_availability(self.library, self.book.isbn)
        
        self.assertTrue(exists)
        self.assertTrue(available)
        self.assertEqual(copies, 3)
        self.assertIn("available", message.lower())

class TestSearch(unittest.TestCase):
    """Test cases for search functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.library = Library()
        
        # Add sample books
        books = [
            Book("123", "Python Programming", "John Smith", 2),
            Book("456", "Java Basics", "Jane Doe", 1),
            Book("789", "Advanced Python", "John Smith", 0),  # No copies
        ]
        
        for book in books:
            self.library.add_book(book)
    
    def test_search_by_title(self):
        """Test searching books by title."""
        results = search_by_title(self.library, "Python")
        
        self.assertEqual(len(results), 2)
        titles = [book.title for book in results]
        self.assertIn("Python Programming", titles)
        self.assertIn("Advanced Python", titles)
    
    def test_search_by_author(self):
        """Test searching books by author."""
        results = search_by_author(self.library, "John Smith")
        
        self.assertEqual(len(results), 2)
        for book in results:
            self.assertEqual(book.author, "John Smith")
    
    def test_search_by_isbn(self):
        """Test searching book by ISBN."""
        result = search_by_isbn(self.library, "123")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.isbn, "123")
        self.assertEqual(result.title, "Python Programming")
    
    def test_search_available_books(self):
        """Test searching only available books."""
        results = search_available_books(self.library, "Python")
        
        self.assertEqual(len(results), 1)  # Only "Python Programming" has copies
        self.assertEqual(results[0].title, "Python Programming")
    
    def test_advanced_search(self):
        """Test advanced search with multiple criteria."""
        results = advanced_search(
            self.library,
            title="Python",
            author="John Smith",
            available_only=True
        )
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Programming")

class TestAuthSystem(unittest.TestCase):
    """Test cases for authentication system."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.auth_system = AuthSystem()
    
    def test_default_users_exist(self):
        """Test that default users are created."""
        # Test librarian login
        success, user_data = self.auth_system.authenticate("librarian", "admin123")
        self.assertTrue(success)
        self.assertEqual(user_data['role'], 'librarian')
        
        # Test member login
        success, user_data = self.auth_system.authenticate("member", "member123")
        self.assertTrue(success)
        self.assertEqual(user_data['role'], 'member')
    
    def test_invalid_login(self):
        """Test login with invalid credentials."""
        success, message = self.auth_system.authenticate("invalid", "password")
        self.assertFalse(success)
        self.assertIn("not found", message.lower())
    
    def test_wrong_password(self):
        """Test login with wrong password."""
        success, message = self.auth_system.authenticate("librarian", "wrong")
        self.assertFalse(success)
        self.assertIn("invalid password", message.lower())
    
    def test_add_new_user(self):
        """Test adding a new user."""
        result = self.auth_system.add_user("newuser", "password", "member")
        self.assertTrue(result)
        
        # Test login with new user
        success, user_data = self.auth_system.authenticate("newuser", "password")
        self.assertTrue(success)
        self.assertEqual(user_data['username'], "newuser")
    
    def test_session_management(self):
        """Test session creation and validation."""
        # Create session
        session_token = self.auth_system.create_session("librarian")
        self.assertIsNotNone(session_token)
        
        # Validate session
        valid, username = self.auth_system.validate_session(session_token)
        self.assertTrue(valid)
        self.assertEqual(username, "librarian")
        
        # Logout
        result = self.auth_system.logout(session_token)
        self.assertTrue(result)
        
        # Validate after logout
        valid, username = self.auth_system.validate_session(session_token)
        self.assertFalse(valid)
    
    def test_password_change(self):
        """Test password change functionality."""
        # Change password
        success, message = self.auth_system.change_password("librarian", "admin123", "newpassword")
        self.assertTrue(success)
        
        # Test old password doesn't work
        success, _ = self.auth_system.authenticate("librarian", "admin123")
        self.assertFalse(success)
        
        # Test new password works
        success, _ = self.auth_system.authenticate("librarian", "newpassword")
        self.assertTrue(success)
    
    def test_simple_authenticate_function(self):
        """Test the simple authenticate function."""
        result = authenticate("librarian", "admin123")
        self.assertTrue(result)
        
        result = authenticate("librarian", "wrong")
        self.assertFalse(result)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.library = Library()
        
        # Add test data
        self.book1 = Book("123", "Test Book 1", "Author 1", 2)
        self.book2 = Book("456", "Test Book 2", "Author 2", 1)
        self.member = Member("M001", "Test Member")
        
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_member(self.member)
    
    def test_complete_workflow(self):
        """Test a complete book issue and return workflow."""
        # Initial state
        self.assertEqual(self.book1.copies, 2)
        self.assertEqual(len(self.member.borrowed_books), 0)
        
        # Issue book
        success, message = issue_book(self.library, self.book1.isbn, self.member)
        self.assertTrue(success)
        self.assertEqual(self.book1.copies, 1)
        self.assertEqual(len(self.member.borrowed_books), 1)
        
        # Search for issued book
        results = search_by_title(self.library, "Test Book 1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].copies, 1)
        
        # Return book
        success, message = return_book(self.library, self.book1.isbn, self.member)
        self.assertTrue(success)
        self.assertEqual(self.book1.copies, 2)
        self.assertEqual(len(self.member.borrowed_books), 0)

def run_tests():
    """
    Run all tests and display results.
    """
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestBook,
        TestMember,
        TestLibrary,
        TestIssueReturn,
        TestSearch,
        TestAuthSystem,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\\nResult: {'PASSED' if success else 'FAILED'}")
    
    return success

if __name__ == '__main__':
    run_tests()