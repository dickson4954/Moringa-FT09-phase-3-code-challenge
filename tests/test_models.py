import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.connection import get_db_connection

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author_name = "John Doe"
        author = Author(author_name)
        self.assertEqual(author.name, author_name) 
    def test_article_creation(self):
        author = Author("John Doe")
        magazine = Magazine("Tech Weekly", "Technology")  
        article = Article(author, magazine, "Test Title", "Test Content")
        self.assertEqual(article.title, "Test Title")


    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly" , "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")

    def test_save_and_get_by_name(self):
        author_name = "John Doe"
        author = Author(author_name)
        author.save()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name FROM authors WHERE id =?
        ''', (author.id,))
        author_name = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(author_name, author_name)
       

    def test_name_change(self):
        author_name = "John Doe"
        author = Author(author_name)
        new_name = "Jane Smith"
        with self.assertRaises(RuntimeError):
            author.name = new_name

    def test_magazine_creation(self):
        magazine = Magazine("Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")
        self.assertIsNone(magazine.id)

    def test_magazine_id_setter_getter(self):
        magazine = Magazine("Tech Weekly", "Technology")
        self.assertIsNone(magazine.id)
        magazine.id = 1
        self.assertEqual(magazine.id, 1)
        with self.assertRaises(ValueError):
            magazine.id = "invalid"  

    def test_magazine_name_setter_getter(self):
        magazine = Magazine("Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")
        with self.assertRaises(TypeError):
            magazine.name = 123  
        with self.assertRaises(ValueError):
            magazine.name = "" 
        with self.assertRaises(ValueError):
            magazine.name = "A" * 17  

    def test_magazine_category_setter_getter(self):
        magazine = Magazine("Tech Weekly", "Technology")
        self.assertEqual(magazine.category, "Technology")
        magazine.category = "Science"
        self.assertEqual(magazine.category, "Science")
        with self.assertRaises(TypeError):
            magazine.category = 123  
        with self.assertRaises(ValueError):
            magazine.category = ""  

    def test_title_property(self):
        author = Author("John Doe")
        magazine = Magazine("Tech Weekly", "Technology")
        article = Article(author, magazine, "Test Title", "Test Content")
        self.assertEqual(article.title, "Test Title")
    def test_article_title_constraints(self):
        author = Author("John Doe")
        magazine = Magazine("Tech Weekly", "Technology")
        with self.assertRaises(ValueError):
            Article(author, magazine, "", "Test Content")
    def test_article_title_immutable(self):
        author = Author("John Doe")
        magazine = Magazine("Tech Weekly", "Technology")
        article = Article(author, magazine, "Test Title", "Test Content")
        with self.assertRaises(AttributeError):
            article.title = "New Title"    
    def test_get_author(self):
        author = Author("John Doe")
        magazine = Magazine("Tech Weekly", "Technology")
        article = Article(author, magazine, "Test Title", "Test Content")
        self.assertEqual(article.author, author)            
    def test_get_magazine(self):
        author = Author("John Doe")
        magazine = Magazine("Tech Weekly", "Technology")
        article = Article(author, magazine, "Test Title", "Test Content")
        self.assertEqual(article.magazine, magazine)
    def test_articles(self):
        author = Author("John Doe")
        author.save()  
        magazine = Magazine("Tech Weekly", "Technology")
        article = Article(author, magazine, "Test Title", "Test Content")
    def test_get_author(self):
        author = Author("John Doe")
        author.save()  
        magazine = Magazine("Tech Weekly", "Technology")
        article = Article(author, magazine, "Test Title", "Test Content")
        self.assertEqual(article.author, author)
    def test_magazine(self):
        author = Author("John Doe")
        author.save()  
        magazine = Magazine("Tech Weekly", "Technology")
        article = Article(author, magazine, "Test Title", "Test Content")
        self.assertEqual(article.magazine, magazine)
    def test_contributors(self):
        author = Author("John Doe")
        author.save()  
        magazine = Magazine("Tech Weekly", "Technology")
        article = Article(author, magazine, "Test Title", "Test Content")

    def test_article_titles(self):
        author = Author("John Doe")
        author.save()  
        magazine = Magazine("Tech Weekly", "Technology")
        article = Article(author, magazine, "Test Title", "Test Content")
        self.assertEqual(article.title, "Test Title")
        
    def test_article_titles_no_articles(self):
        author = Author("John Doe")
        author.save()  
        magazine = Magazine("Tech Weekly", "Technology")
        article = Article(author, magazine, "Test Title", "Test Content")
        self.assertEqual(article.title, "Test Title")

    def test_contributing_authors(self):
        author = Author("John Doe")
        author.save()
        magazine = Magazine("Tech Weekly", "Technology")
        magazine.id = 123
        article = Article(author, magazine, "Test Title", "Test Content")
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.author, author)

    def test_contributing_authors_none(self):
        author = Author("John Doe")
        author.save()
        magazine = Magazine("Tech Weekly", "Technology")
        magazine.id = 123
        article = Article(author, magazine, "Test Title", "Test Content")

        

        
if __name__ == "__main__":
    unittest.main()
