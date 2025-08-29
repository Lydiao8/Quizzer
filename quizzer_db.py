import sqlite3

class QuizzerDB:
    def __init__(self, db_path="Quizzer.db"):
        self.db_path = db_path
        self._initialize_tables()
        self._seed_question_data()

    def _initialize_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create questionDB table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questionDB (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                options TEXT,
                answer TEXT
            )
        ''')

        # Create candidatesDB table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidatesDB (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                firstName TEXT,
                lastName TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def _seed_question_data(self):
        questionDB = {
            1: {"Question": "What is the function for viewing a companies financial statement?", "Options": "FA,EE,ANR,EEB", "Answer": "FA"}, 
            2: {"Question": "What is the function for peer analysis?", "Options": "FA,EE,ANR,EEB", "Answer": "RV" },
            3: {"Question": "What is the best function for analysis of peer KPIs", "Options": "FA,KPIC,RV,EEB", "Answer": "KPIC"},
            4: {"Question": "What function is good for top down analysis", "Options": "GRR,IMAP,WATC,All of the above", "Answer": "All of the above"},
            5: {"Question": "What function shows the surprise from earning announcement?", "Options": "FA,ERN,EEB,MODL", "Answer": "ERN"}
        }

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM questionDB")
        count = cursor.fetchone()[0]

        if count == 0:  # Seed only if the table is empty
            questionDBtuples = [
                (details["Question"], details["Options"], details["Answer"])
                for ID, details in questionDB.items()
            ]

            cursor.executemany(
                'INSERT INTO questionDB (question, options, answer) VALUES (?, ?, ?)',
                questionDBtuples
            )
            conn.commit()

        conn.close()
       
    
    def create_candidate(self, candidate_details):
        firstname = candidate_details.firstName
        lastname = candidate_details.lastName
        email = candidate_details.email

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try: 
            cursor.execute(
            '''
            INSERT INTO candidatesDB (email, firstName, lastName) 
            VALUES (?, ?, ?)
            ''',
                (email, firstname, lastname)
            )
            conn.commit()

            result = {"message": "Candidate created successfully."}
    
        except Exception as e:
            result = {"error": str(e)}
        
        finally: 
            conn.close()
        
        return result
    
    def get_questions(self): 
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, question, options, answer FROM questionDB;")
        result = cursor.fetchall()
        conn.close()
        return result
    
    def add_question(self, question_details):
        question = question_details.question
        options = question_details.options
        answer = question_details.answer

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                '''
                INSERT INTO questionDB (question, options, answer) 
                VALUES (?, ?, ?)
                ''',
                (question, options, answer)
            )
            conn.commit()

            return {"message": "Question added successfully!"}
 
        except Exception as e:
            return {"error": str(e)}
    
        finally: 
            conn.close()
        
        return result
