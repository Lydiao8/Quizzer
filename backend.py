from fastapi import FastAPI

from QuestionsAPI import get_all_questions

backEndApp = FastAPI()

@backEndApp.get("/end_point_1")
def end_point_1():
    return get_all_questions()
