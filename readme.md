Framework:
1. I used FastApi to make my project.
2. We need to make virtual environment. Command: py -m venv virtual_env
3. to start server we have to activate virtual environment.(virtual_env/Scripts/activate.bat)
4. Then pip install -r requirements.txt
5. now we can launch the server with uvicorn main:app
6. we can easy check functions with automatic documentation( http://127.0.0.1:8000/docs)
7. I chose json data for saving reponses.