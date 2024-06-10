from database.connection import get_db_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("ID must be of type int")
        self._id = value

   

    @property
    def name(self):
        return self._name

    @name.setter 
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be of type str")
        if len(value) == 0 or len(value) > 16:
            raise ValueError("Name must be between 1 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value:str):
        # if not isinstance(value, str):
        #     raise TypeError("Category must be of type str")
        if len(value) == 0:
            raise ValueError("Category must be longer than 0 characters")
        self._category = value

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT articles.title FROM articles 
            INNER JOIN magazines ON articles.magazine_id = magazines.id 
            WHERE magazines.id = ?
        ''', (self.id,))
        
        articles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return articles

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT authors.name FROM articles 
            INNER JOIN magazines ON articles.magazine_id = magazines.id 
            INNER JOIN authors ON articles.author_id = authors.id 
            WHERE magazines.id = ?
        ''', (self.id,))
        
        contributors = [row[0] for row in cursor.fetchall()]
        conn.close()
        return contributors
    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title FROM articles WHERE magazine_id = ?
        ''', (self.id,))
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        if not titles:
           return None
        else:
            return titles
        
    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.id, authors.name
            FROM articles
            INNER JOIN authors ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(*) > 2
        ''', (self.id,))
        authors_rows = cursor.fetchall()
        conn.close()
        
        if not authors_rows:
            return None

        contributing_authors = [Author(row['id'], row['name']) for row in authors_rows if type(row) is Author]
        return contributing_authors  
    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO magazines (name,category) VALUES (?,?)
        ''', (self.name,self.category))
        self.id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def get_by_name(cls, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM authors WHERE name = ?
        ''', (name,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return cls(row['name'])
        return None
    

    def __repr__(self):
        return f'<Magazine {self.name}>'
