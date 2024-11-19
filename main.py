from fastapi import FastAPI
app = FastAPI()


@app.get("/start-test")
def handle_request_from_external_clients():
    return ["Hello world"]

@app.get("/start-test/{user_name}")
def read_item(user_name):
    return "Hello, Dear" + user_name
