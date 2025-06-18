from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect('Quizzer.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS questionDB(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    question TEXT, 
                    options TEXT, 
                    answer TEXT)'''
                )

cursor.execute('''CREATE TABLE IF NOT EXISTS candidatesDB(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT, 
                    firstName TEXT, 
                    lastName TEXT)'''
                )

conn.commit()


# questionDB = {
#     1 : {"Question": "What is the function for viewing a companies financial statement?", "Options": "FA,EE,ANR,EEB", "Answer": "FA"}, 
#     2 : {"Question": "What is the function for peer analysis?", "Options": "FA,EE,ANR,EEB", "Answer": "RV" },
#     3 : {"Question": "What is the best function for analysis of peer KPIs", "Options": "FA,KPIC,RV,EEB", "Answer": "KPIC"},
#     4 : {"Question": "What function is good for top down analysis", "Options": "GRR,IMAP,WATC,All of the above", "Answer": "All of the above"},
#     5 : {"Question": "What function shows the surprise from earning announcement?", "Options": "FA,ERN,EEB,MODL", "Answer": "ERN"}
# }

# questionDBtuples = [
#     (details["Question"], details["Options"], details["Answer"])
#     for ID, details in questionDB.items()
# ] 

# cursor.executemany('INSERT INTO questionDB (question, options, answer) VALUES (?,?,?)', questionDBtuples) #if statement to check if questions are in database? 
# conn.commit()
conn.close()

class RegisterCandidateRequest(BaseModel): 
    firstName: str
    lastName: str
    email: str

class NewQuestion(BaseModel): 
    question: str
    options: str
    answer: str

class Quizzer: 
    def __init__(self): 
        self.questionsDict = {}
        self.current = 0
        self.score = 0 

    def load_questions(self):
        conn = sqlite3.connect('Quizzer.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, question, options, answer FROM questionDB;")
        dbItems = cursor.fetchall()

        for question_no, question, options, answer in dbItems:
            self.questionsDict[question_no] = [question, options.split(','), answer]
        
        conn.close() #how is it returning the options? 
    
    def get_next_question(self):
        self.current += 1
        if self.current > len(self.questionsDict):
            return {"message": f"Your score is {self.score} out of {len(self.questionsDict)}"} #function to get final score 
        question, options, answer = self.questionsDict[self.current]
        return {"question": question, "options": options}
    
    def evaluate_answer(self, user_answer):
        correct_answer = self.questionsDict[self.current][2]
        if user_answer.lower() == correct_answer.lower():  
            self.score += 1
    
    def end_quizzer(self): #should it be an end point too?
        self.score = 0 
        self.current = 0 
        self.questionsDict = {}


quizzer_instances = {}

@app.post("/candidates/create")
def create_candidate(candidate: RegisterCandidateRequest): # Insert candidate details into the database
    conn = sqlite3.connect('Quizzer.db')
    cursor = conn.cursor()

    try: 
        cursor.execute(
        '''
        INSERT INTO candidatesDB (email, firstName, lastName) 
        VALUES (?, ?, ?)
        ''',
            (candidate.email, candidate.firstName, candidate.lastName)
        )
        conn.commit()
        quizzer = Quizzer()
        quizzer.load_questions()
        quizzer_instances[candidate.email] = quizzer

        return {"message": "Candidate created successfully."}
    
    except Exception as e:
        return {"error": str(e)}

    # Initialize a new quizzer instance for the candidate
    conn.close()

    
@app.get("/start-test")
def start_quiz(email: str):
    quizzer = quizzer_instances[email]
    return quizzer.get_next_question()

@app.get("/next-question")
def next_question(email: str):
    quizzer = quizzer_instances[email]
    return quizzer.get_next_question()

@app.get("/submit-answer")
def get_answer(email: str, user_answer: str): 
    quizzer = quizzer_instances[email]
    quizzer.evaluate_answer(user_answer)

@app.post("/add-question")
def add_question(new_question: NewQuestion):
    conn = sqlite3.connect('Quizzer.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            '''
            INSERT INTO questionDB (question, options, answer) 
            VALUES (?, ?, ?)
            ''',
            (new_question.question, new_question.options, new_question.answer)
        )
        conn.commit()

        return {"message": "Question added successfully!"}
 
    except Exception as e:
        return {"error": str(e)}
    
    conn.close()

@app.delete("/end-quiz")
def end_quizzer(email: str):
    if email in quizzer_instances: 
        quizzer = quizzer_instances[email]
        quizzer.end_quizzer() 
        del quizzer_instances[email]
        return {"message": "Quiz ended!"}
    return {"message": "No quiz has been started"}


# can candidate submit without answering all questions? 
# end point to submit?     
# end point to update/delete from question database


