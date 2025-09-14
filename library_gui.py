"""
Graphical User Interface for Library Management System
A modern tkinter-based GUI for the library management system.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import threading

# Import our modules
from book import Book
from member import Member
from library import Library
from issue_return import (
    issue_book, return_book, issue_book_by_id, return_book_by_id,
    get_member_borrowed_books, check_book_availability
)
from search import (
    search_books, search_available_books, advanced_search
)
from auth_system import AuthSystem

class LoginWindow:
    """Login window for user authentication."""
    
    def __init__(self, parent, auth_system, callback):
        """
        Initialize login window.
        
        Args:
            parent: Parent window
            auth_system: Authentication system instance
            callback: Function to call after successful login
        """
        self.parent = parent
        self.auth_system = auth_system
        self.callback = callback
        self.login_window = None
        self.create_login_window()
    
    def create_login_window(self):
        """Create and display login window."""
        self.login_window = tk.Toplevel(self.parent)
        self.login_window.title("Library Management System - Login")
        self.login_window.geometry("400x300")
        self.login_window.resizable(False, False)
        
        # Center the window
        self.login_window.transient(self.parent)
        self.login_window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(self.login_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Library Management System", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Login form
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        # Username
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(form_frame, width=20, font=("Arial", 11))
        self.username_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        # Password
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(form_frame, width=20, show="*", font=("Arial", 11))
        self.password_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        # Login button
        login_btn = ttk.Button(form_frame, text="Login", command=self.login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Default credentials info
        info_frame = ttk.LabelFrame(main_frame, text="Default Credentials", padding="10")
        info_frame.pack(pady=20, fill="x")
        
        ttk.Label(info_frame, text="Librarian: librarian / admin123").pack(anchor="w")
        ttk.Label(info_frame, text="Member: member / member123").pack(anchor="w")
        
        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Focus on username entry
        self.username_entry.focus()
    
    def login(self):
        """Handle login attempt."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return
        
        success, user_data = self.auth_system.authenticate(username, password)
        
        if success:
            session_token = self.auth_system.create_session(username)
            self.login_window.destroy()
            self.callback(user_data, session_token)
        else:
            messagebox.showerror("Login Failed", user_data)
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()

class LibraryGUI:
    """Main GUI application for Library Management System."""
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Initialize system components
        self.library = Library()
        self.auth_system = AuthSystem()
        self.current_user = None
        self.session_token = None
        
        # Load sample data
        self._load_sample_data()
        
        # Create main interface
        self.create_main_interface()
        
        # Show login window
        self.show_login()
    
    def _load_sample_data(self):
        """Load sample data for demonstration."""
        # Sample books
        books = [
            Book("978-0134685991", "Effective Java", "Joshua Bloch", 3),
            Book("978-0596009205", "Head First Design Patterns", "Eric Freeman", 2),
            Book("978-0132350884", "Clean Code", "Robert C. Martin", 4),
            Book("978-0201616224", "The Pragmatic Programmer", "Andrew Hunt", 2),
            Book("978-0134494166", "Clean Architecture", "Robert C. Martin", 1),
            Book("978-0134052501", "Design Patterns", "Gang of Four", 2),
            Book("978-0321125217", "Domain-Driven Design", "Eric Evans", 1),
            Book("978-0596007124", "Beautiful Code", "Andy Oram", 3),
        ]
        
        for book in books:
            self.library.add_book(book)
        
        # Sample members
        members = [
            Member("M001", "Alice Johnson"),
            Member("M002", "Bob Smith"),
            Member("M003", "Charlie Brown"),
            Member("M004", "Diana Prince"),
            Member("M005", "Edward Norton"),
        ]
        
        for member in members:
            self.library.add_member(member)
    
    def create_main_interface(self):
        """Create the main application interface."""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header frame
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        # User info label
        self.user_label = ttk.Label(self.header_frame, text="Not logged in", 
                                   font=("Arial", 12, "bold"))
        self.user_label.pack(side="left")
        
        # Logout button
        self.logout_btn = ttk.Button(self.header_frame, text="Logout", 
                                    command=self.logout, state="disabled")
        self.logout_btn.pack(side="right")
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs (initially empty)
        self.create_search_tab()
        self.create_books_tab()
        self.create_members_tab()
        self.create_transactions_tab()
        self.create_statistics_tab()
    
    def create_search_tab(self):
        """Create search tab."""
        self.search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_frame, text="📚 Search Books")
        
        # Search controls
        search_controls = ttk.LabelFrame(self.search_frame, text="Search Options", padding="10")
        search_controls.pack(fill="x", padx=10, pady=10)
        
        # Search type
        ttk.Label(search_controls, text="Search by:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.search_type = ttk.Combobox(search_controls, values=["All", "Title", "Author", "ISBN"], 
                                       state="readonly", width=15)
        self.search_type.set("All")
        self.search_type.grid(row=0, column=1, padx=(0, 20))
        
        # Search entry
        ttk.Label(search_controls, text="Search term:").grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.search_entry = ttk.Entry(search_controls, width=30)
        self.search_entry.grid(row=0, column=3, padx=(0, 10))
        
        # Search button
        search_btn = ttk.Button(search_controls, text="Search", command=self.search_books)
        search_btn.grid(row=0, column=4)
        
        # Available only checkbox
        self.available_only = tk.BooleanVar()
        available_cb = ttk.Checkbutton(search_controls, text="Available only", 
                                      variable=self.available_only)
        available_cb.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))
        
        # Results frame
        results_frame = ttk.LabelFrame(self.search_frame, text="Search Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Results treeview
        columns = ("ISBN", "Title", "Author", "Copies", "Status")
        self.search_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=150)
        
        # Scrollbars
        search_scrollbar_v = ttk.Scrollbar(results_frame, orient="vertical", command=self.search_tree.yview)
        search_scrollbar_h = ttk.Scrollbar(results_frame, orient="horizontal", command=self.search_tree.xview)
        self.search_tree.configure(yscrollcommand=search_scrollbar_v.set, xscrollcommand=search_scrollbar_h.set)
        
        self.search_tree.pack(side="left", fill=tk.BOTH, expand=True)
        search_scrollbar_v.pack(side="right", fill="y")
        search_scrollbar_h.pack(side="bottom", fill="x")
        
        # Bind Enter key to search
        self.search_entry.bind("<Return>", lambda e: self.search_books())
    
    def create_books_tab(self):
        """Create books management tab."""
        self.books_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.books_frame, text="📖 Books")
        
        # Controls frame
        controls_frame = ttk.Frame(self.books_frame)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        # Add book button
        self.add_book_btn = ttk.Button(controls_frame, text="➕ Add Book", 
                                      command=self.show_add_book_dialog)
        self.add_book_btn.pack(side="left", padx=(0, 10))
        
        # Remove book button
        self.remove_book_btn = ttk.Button(controls_frame, text="🗑️ Remove Book", 
                                         command=self.remove_selected_book)
        self.remove_book_btn.pack(side="left", padx=(0, 10))
        
        # Refresh button
        refresh_books_btn = ttk.Button(controls_frame, text="🔄 Refresh", 
                                      command=self.refresh_books_list)
        refresh_books_btn.pack(side="left")
        
        # Books list frame
        books_list_frame = ttk.LabelFrame(self.books_frame, text="All Books", padding="10")
        books_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Books treeview
        books_columns = ("ISBN", "Title", "Author", "Copies", "Status")
        self.books_tree = ttk.Treeview(books_list_frame, columns=books_columns, show="headings", height=20)
        
        for col in books_columns:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=150)
        
        # Scrollbars for books tree
        books_scrollbar_v = ttk.Scrollbar(books_list_frame, orient="vertical", command=self.books_tree.yview)
        books_scrollbar_h = ttk.Scrollbar(books_list_frame, orient="horizontal", command=self.books_tree.xview)
        self.books_tree.configure(yscrollcommand=books_scrollbar_v.set, xscrollcommand=books_scrollbar_h.set)
        
        self.books_tree.pack(side="left", fill=tk.BOTH, expand=True)
        books_scrollbar_v.pack(side="right", fill="y")
        books_scrollbar_h.pack(side="bottom", fill="x")
    
    def create_members_tab(self):
        """Create members management tab."""
        self.members_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.members_frame, text="👥 Members")
        
        # Controls frame
        members_controls_frame = ttk.Frame(self.members_frame)
        members_controls_frame.pack(fill="x", padx=10, pady=10)
        
        # Add member button
        self.add_member_btn = ttk.Button(members_controls_frame, text="➕ Add Member", 
                                        command=self.show_add_member_dialog)
        self.add_member_btn.pack(side="left", padx=(0, 10))
        
        # Remove member button
        self.remove_member_btn = ttk.Button(members_controls_frame, text="🗑️ Remove Member", 
                                           command=self.remove_selected_member)
        self.remove_member_btn.pack(side="left", padx=(0, 10))
        
        # Refresh button
        refresh_members_btn = ttk.Button(members_controls_frame, text="🔄 Refresh", 
                                        command=self.refresh_members_list)
        refresh_members_btn.pack(side="left")
        
        # Members list frame
        members_list_frame = ttk.LabelFrame(self.members_frame, text="All Members", padding="10")
        members_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Members treeview
        members_columns = ("Member ID", "Name", "Books Borrowed")
        self.members_tree = ttk.Treeview(members_list_frame, columns=members_columns, show="headings", height=20)
        
        for col in members_columns:
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=200)
        
        # Scrollbars for members tree
        members_scrollbar_v = ttk.Scrollbar(members_list_frame, orient="vertical", command=self.members_tree.yview)
        self.members_tree.configure(yscrollcommand=members_scrollbar_v.set)
        
        self.members_tree.pack(side="left", fill=tk.BOTH, expand=True)
        members_scrollbar_v.pack(side="right", fill="y")
    
    def create_transactions_tab(self):
        """Create transactions (issue/return) tab."""
        self.transactions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.transactions_frame, text="🔄 Issue/Return")
        
        # Issue book frame
        issue_frame = ttk.LabelFrame(self.transactions_frame, text="Issue Book", padding="10")
        issue_frame.pack(fill="x", padx=10, pady=10)
        
        # Issue book controls
        ttk.Label(issue_frame, text="Book ISBN:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.issue_isbn_entry = ttk.Entry(issue_frame, width=20)
        self.issue_isbn_entry.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(issue_frame, text="Member ID:").grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.issue_member_entry = ttk.Entry(issue_frame, width=15)
        self.issue_member_entry.grid(row=0, column=3, padx=(0, 20))
        
        self.issue_book_btn = ttk.Button(issue_frame, text="Issue Book", command=self.issue_book)
        self.issue_book_btn.grid(row=0, column=4)
        
        # Return book frame
        return_frame = ttk.LabelFrame(self.transactions_frame, text="Return Book", padding="10")
        return_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Return book controls
        ttk.Label(return_frame, text="Book ISBN:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.return_isbn_entry = ttk.Entry(return_frame, width=20)
        self.return_isbn_entry.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(return_frame, text="Member ID:").grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.return_member_entry = ttk.Entry(return_frame, width=15)
        self.return_member_entry.grid(row=0, column=3, padx=(0, 20))
        
        self.return_book_btn = ttk.Button(return_frame, text="Return Book", command=self.return_book)
        self.return_book_btn.grid(row=0, column=4)
        
        # Transaction history frame
        history_frame = ttk.LabelFrame(self.transactions_frame, text="Current Borrowed Books", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Borrowed books treeview
        borrowed_columns = ("Member ID", "Member Name", "ISBN", "Book Title", "Author")
        self.borrowed_tree = ttk.Treeview(history_frame, columns=borrowed_columns, show="headings", height=15)
        
        for col in borrowed_columns:
            self.borrowed_tree.heading(col, text=col)
            self.borrowed_tree.column(col, width=150)
        
        # Scrollbars for borrowed tree
        borrowed_scrollbar_v = ttk.Scrollbar(history_frame, orient="vertical", command=self.borrowed_tree.yview)
        self.borrowed_tree.configure(yscrollcommand=borrowed_scrollbar_v.set)
        
        self.borrowed_tree.pack(side="left", fill=tk.BOTH, expand=True)
        borrowed_scrollbar_v.pack(side="right", fill="y")
        
        # Refresh borrowed books
        refresh_borrowed_btn = ttk.Button(history_frame, text="🔄 Refresh", 
                                         command=self.refresh_borrowed_books)
        refresh_borrowed_btn.pack(side="bottom", pady=(10, 0))
    
    def create_statistics_tab(self):
        """Create statistics tab."""
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="📊 Statistics")
        
        # Statistics display
        stats_display_frame = ttk.LabelFrame(self.stats_frame, text="Library Statistics", padding="20")
        stats_display_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create statistics labels
        self.stats_labels = {}
        stats_items = [
            ("Total Books", "total_books"),
            ("Available Books", "available_books"),
            ("Total Members", "total_members"),
            ("Books Currently Borrowed", "books_borrowed")
        ]
        
        for i, (label_text, key) in enumerate(stats_items):
            ttk.Label(stats_display_frame, text=f"{label_text}:", 
                     font=("Arial", 12, "bold")).grid(row=i, column=0, sticky="w", pady=10, padx=(0, 20))
            
            self.stats_labels[key] = ttk.Label(stats_display_frame, text="0", 
                                              font=("Arial", 12))
            self.stats_labels[key].grid(row=i, column=1, sticky="w", pady=10)
        
        # Refresh stats button
        refresh_stats_btn = ttk.Button(stats_display_frame, text="🔄 Refresh Statistics", 
                                      command=self.refresh_statistics)
        refresh_stats_btn.grid(row=len(stats_items), column=0, columnspan=2, pady=20)
    
    def show_login(self):
        """Show login window."""
        LoginWindow(self.root, self.auth_system, self.on_login_success)
    
    def on_login_success(self, user_data, session_token):
        """Handle successful login."""
        self.current_user = user_data
        self.session_token = session_token
        
        # Update UI
        user_info = f"Logged in as: {user_data['info'].get('name', user_data['username'])} ({user_data['role'].title()})"
        self.user_label.config(text=user_info)
        self.logout_btn.config(state="normal")
        
        # Configure tabs based on role
        self.configure_tabs_for_role()
        
        # Load initial data
        self.refresh_all_data()
        
        messagebox.showinfo("Login Successful", f"Welcome, {user_data['info'].get('name', user_data['username'])}!")
    
    def configure_tabs_for_role(self):
        """Configure available tabs based on user role."""
        if self.current_user['role'] == 'librarian':
            # Librarians can access all tabs
            for i in range(self.notebook.index("end")):
                self.notebook.tab(i, state="normal")
            
            # Enable all buttons
            self.add_book_btn.config(state="normal")
            self.remove_book_btn.config(state="normal")
            self.add_member_btn.config(state="normal")
            self.remove_member_btn.config(state="normal")
            self.issue_book_btn.config(state="normal")
            self.return_book_btn.config(state="normal")
        
        else:  # member
            # Members can only access search and statistics
            self.notebook.tab(0, state="normal")  # Search
            self.notebook.tab(1, state="disabled")  # Books management
            self.notebook.tab(2, state="disabled")  # Members management
            self.notebook.tab(3, state="disabled")  # Transactions
            self.notebook.tab(4, state="normal")  # Statistics
            
            # Disable management buttons
            self.add_book_btn.config(state="disabled")
            self.remove_book_btn.config(state="disabled")
            self.add_member_btn.config(state="disabled")
            self.remove_member_btn.config(state="disabled")
            self.issue_book_btn.config(state="disabled")
            self.return_book_btn.config(state="disabled")
            
            # Switch to search tab
            self.notebook.select(0)
    
    def logout(self):
        """Handle user logout."""
        if self.session_token:
            self.auth_system.logout(self.session_token)
        
        self.current_user = None
        self.session_token = None
        
        # Update UI
        self.user_label.config(text="Not logged in")
        self.logout_btn.config(state="disabled")
        
        # Clear all data
        self.clear_all_data()
        
        # Show login window
        self.show_login()
    
    def refresh_all_data(self):
        """Refresh all data displays."""
        self.refresh_books_list()
        self.refresh_members_list()
        self.refresh_borrowed_books()
        self.refresh_statistics()
    
    def clear_all_data(self):
        """Clear all data from displays."""
        self.search_tree.delete(*self.search_tree.get_children())
        self.books_tree.delete(*self.books_tree.get_children())
        self.members_tree.delete(*self.members_tree.get_children())
        self.borrowed_tree.delete(*self.borrowed_tree.get_children())
        
        for key in self.stats_labels:
            self.stats_labels[key].config(text="0")
    
    def search_books(self):
        """Search for books and display results."""
        search_term = self.search_entry.get().strip()
        search_type = self.search_type.get().lower()
        available_only = self.available_only.get()
        
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term.")
            return
        
        # Clear previous results
        self.search_tree.delete(*self.search_tree.get_children())
        
        # Perform search
        if available_only:
            results = search_available_books(self.library, search_term, search_type)
        else:
            results = search_books(self.library, search_term, search_type)
        
        # Display results
        for book in results:
            status = "Available" if book.copies > 0 else "Not Available"
            self.search_tree.insert("", "end", values=(
                book.isbn, book.title, book.author, book.copies, status
            ))
        
        # Show result count
        result_count = len(results)
        messagebox.showinfo("Search Results", f"Found {result_count} book(s) matching your search.")
    
    def refresh_books_list(self):
        """Refresh the books list."""
        self.books_tree.delete(*self.books_tree.get_children())
        
        for book in self.library.list_books():
            status = "Available" if book.copies > 0 else "Not Available"
            self.books_tree.insert("", "end", values=(
                book.isbn, book.title, book.author, book.copies, status
            ))
    
    def refresh_members_list(self):
        """Refresh the members list."""
        self.members_tree.delete(*self.members_tree.get_children())
        
        for member in self.library.list_members():
            self.members_tree.insert("", "end", values=(
                member.member_id, member.name, len(member.borrowed_books)
            ))
    
    def refresh_borrowed_books(self):
        """Refresh the borrowed books list."""
        self.borrowed_tree.delete(*self.borrowed_tree.get_children())
        
        for member in self.library.list_members():
            for isbn in member.borrowed_books:
                book = self.library.get_book(isbn)
                if book:
                    self.borrowed_tree.insert("", "end", values=(
                        member.member_id, member.name, isbn, book.title, book.author
                    ))
    
    def refresh_statistics(self):
        """Refresh library statistics."""
        stats = self.library.get_library_stats()
        
        for key, value in stats.items():
            if key in self.stats_labels:
                self.stats_labels[key].config(text=str(value))
    
    def show_add_book_dialog(self):
        """Show dialog to add a new book."""
        dialog = AddBookDialog(self.root, self.library, self.refresh_books_list)
    
    def show_add_member_dialog(self):
        """Show dialog to add a new member."""
        dialog = AddMemberDialog(self.root, self.library, self.refresh_members_list)
    
    def remove_selected_book(self):
        """Remove selected book from library."""
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a book to remove.")
            return
        
        item = self.books_tree.item(selection[0])
        isbn = item['values'][0]
        title = item['values'][1]
        
        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{title}'?"):
            success = self.library.remove_book(isbn)
            if success:
                messagebox.showinfo("Success", "Book removed successfully!")
                self.refresh_books_list()
                self.refresh_statistics()
            else:
                messagebox.showerror("Error", "Failed to remove book.")
    
    def remove_selected_member(self):
        """Remove selected member from library."""
        selection = self.members_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a member to remove.")
            return
        
        item = self.members_tree.item(selection[0])
        member_id = item['values'][0]
        name = item['values'][1]
        books_borrowed = item['values'][2]
        
        if books_borrowed > 0:
            messagebox.showerror("Error", f"Cannot remove member '{name}' - they have {books_borrowed} book(s) borrowed.")
            return
        
        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove member '{name}'?"):
            success = self.library.remove_member(member_id)
            if success:
                messagebox.showinfo("Success", "Member removed successfully!")
                self.refresh_members_list()
                self.refresh_statistics()
            else:
                messagebox.showerror("Error", "Failed to remove member.")
    
    def issue_book(self):
        """Issue a book to a member."""
        isbn = self.issue_isbn_entry.get().strip()
        member_id = self.issue_member_entry.get().strip()
        
        if not isbn or not member_id:
            messagebox.showerror("Error", "Please enter both ISBN and Member ID.")
            return
        
        success, message = issue_book_by_id(self.library, isbn, member_id)
        
        if success:
            messagebox.showinfo("Success", message)
            self.issue_isbn_entry.delete(0, tk.END)
            self.issue_member_entry.delete(0, tk.END)
            self.refresh_all_data()
        else:
            messagebox.showerror("Error", message)
    
    def return_book(self):
        """Return a book from a member."""
        isbn = self.return_isbn_entry.get().strip()
        member_id = self.return_member_entry.get().strip()
        
        if not isbn or not member_id:
            messagebox.showerror("Error", "Please enter both ISBN and Member ID.")
            return
        
        success, message = return_book_by_id(self.library, isbn, member_id)
        
        if success:
            messagebox.showinfo("Success", message)
            self.return_isbn_entry.delete(0, tk.END)
            self.return_member_entry.delete(0, tk.END)
            self.refresh_all_data()
        else:
            messagebox.showerror("Error", message)
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

class AddBookDialog:
    """Dialog for adding a new book."""
    
    def __init__(self, parent, library, callback):
        """
        Initialize add book dialog.
        
        Args:
            parent: Parent window
            library: Library instance
            callback: Function to call after adding book
        """
        self.parent = parent
        self.library = library
        self.callback = callback
        self.create_dialog()
    
    def create_dialog(self):
        """Create and display the dialog."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add New Book")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        ttk.Label(main_frame, text="ISBN:").grid(row=0, column=0, sticky="w", pady=5)
        self.isbn_entry = ttk.Entry(main_frame, width=30)
        self.isbn_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Title:").grid(row=1, column=0, sticky="w", pady=5)
        self.title_entry = ttk.Entry(main_frame, width=30)
        self.title_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Author:").grid(row=2, column=0, sticky="w", pady=5)
        self.author_entry = ttk.Entry(main_frame, width=30)
        self.author_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Copies:").grid(row=3, column=0, sticky="w", pady=5)
        self.copies_entry = ttk.Entry(main_frame, width=30)
        self.copies_entry.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Add Book", command=self.add_book).pack(side="left", padx=(0, 10))
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side="left")
        
        # Focus on first entry
        self.isbn_entry.focus()
    
    def add_book(self):
        """Add the book to the library."""
        isbn = self.isbn_entry.get().strip()
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        copies_str = self.copies_entry.get().strip()
        
        # Validation
        if not all([isbn, title, author, copies_str]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        if self.library.get_book(isbn):
            messagebox.showerror("Error", "Book with this ISBN already exists.")
            return
        
        try:
            copies = int(copies_str)
            if copies < 0:
                messagebox.showerror("Error", "Number of copies cannot be negative.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for copies.")
            return
        
        # Add book
        book = Book(isbn, title, author, copies)
        self.library.add_book(book)
        
        messagebox.showinfo("Success", f"Book '{title}' added successfully!")
        self.callback()
        self.dialog.destroy()

class AddMemberDialog:
    """Dialog for adding a new member."""
    
    def __init__(self, parent, library, callback):
        """
        Initialize add member dialog.
        
        Args:
            parent: Parent window
            library: Library instance
            callback: Function to call after adding member
        """
        self.parent = parent
        self.library = library
        self.callback = callback
        self.create_dialog()
    
    def create_dialog(self):
        """Create and display the dialog."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add New Member")
        self.dialog.geometry("350x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        ttk.Label(main_frame, text="Member ID:").grid(row=0, column=0, sticky="w", pady=5)
        self.member_id_entry = ttk.Entry(main_frame, width=25)
        self.member_id_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(main_frame, width=25)
        self.name_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Add Member", command=self.add_member).pack(side="left", padx=(0, 10))
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side="left")
        
        # Focus on first entry
        self.member_id_entry.focus()
    
    def add_member(self):
        """Add the member to the library."""
        member_id = self.member_id_entry.get().strip()
        name = self.name_entry.get().strip()
        
        # Validation
        if not member_id or not name:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        if self.library.get_member(member_id):
            messagebox.showerror("Error", "Member with this ID already exists.")
            return
        
        # Add member
        member = Member(member_id, name)
        self.library.add_member(member)
        
        messagebox.showinfo("Success", f"Member '{name}' added successfully!")
        self.callback()
        self.dialog.destroy()

def main():
    """Main function to start the GUI application."""
    app = LibraryGUI()
    app.run()

if __name__ == "__main__":
    main()