from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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
        dbItems = QuizzerDB.get_questions()

        for question_no, question, options, answer in dbItems:
            self.questionsDict[question_no] = [question, options.split(','), answer]
        
        #how is it returning the options? 
    
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
    return QuizzerDB.create_candidate(candidate)

    
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
    return QuizzerDB.add_question(new_question)

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


