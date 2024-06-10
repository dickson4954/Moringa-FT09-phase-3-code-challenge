from database.connection import get_db_connection

class Author:
    def __init__(self, name):
        self.name = name
        self._id = None
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, int):
            self._id = value
        else:
            raise TypeError("ID must be of type int")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value) > 0:
            if not hasattr(self, '_name'):
                self._name = value
            else:
                raise RuntimeError("Name cannot be changed after author is instantiated")
        else:
            raise ValueError("Name must be a non-empty string")

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT articles.title FROM articles 
            INNER JOIN authors ON articles.author_id = authors.id 
            WHERE authors.id = ?
        ''', (self.id,))
        
        articles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return articles

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT DISTINCT magazines.name FROM articles 
            INNER JOIN authors ON articles.author_id = authors.id 
            INNER JOIN magazines ON articles.magazine_id = magazines.id 
            WHERE authors.id = ?
        ''', (self.id,))

        magazines = [row[0] for row in cursor.fetchall()]
        conn.close()
        return magazines

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO authors (name) VALUES (?)
        ''', (self.name,))
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
