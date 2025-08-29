from fastapi import FastAPI
from pydantic import BaseModel
from quizzer_db import QuizzerDB

app = FastAPI()
db = QuizzerDB()

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
        dbItems = db.get_questions()

        for question_no, question, options, answer in dbItems:
            self.questionsDict[question_no] = [question, options.split(','), answer]
        
    
    def get_next_question(self):
        self.current += 1
        if self.current > len(self.questionsDict):
            return {"message": f"Your score is {self.score} out of {len(self.questionsDict)}"} 
        question, options, answer = self.questionsDict[self.current]
        return {"question": question, "options": options}
    
    def evaluate_answer(self, user_answer):
        correct_answer = self.questionsDict[self.current][2]
        if user_answer.lower() == correct_answer.lower():  
            self.score += 1
    
    def end_quizzer(self): 
        self.score = 0 
        self.current = 0 
        self.questionsDict = {}


quizzer_instances = {}

@app.post("/candidates/create")
def create_candidate(candidate: RegisterCandidateRequest): # Insert candidate details into the database
    return db.create_candidate(candidate)

    
@app.get("/start-test")
def start_quiz(email: str):
    quizzer_instances[email] = Quizzer() #to check logic here3
    quizzer_instances[email].load_questions()
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
    return db.add_question(new_question)

@app.delete("/end-quiz")
def end_quizzer(email: str):
    if email in quizzer_instances: 
        quizzer = quizzer_instances[email]
        quizzer.end_quizzer() 
        del quizzer_instances[email]
        return {"message": "Quiz ended!"}
    return {"message": "No quiz has been started"}




