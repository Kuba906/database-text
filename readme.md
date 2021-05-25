live demo: https://da-plu-2021-jakubszuper.herokuapp.com/
1. Framework:
- I chose Fastapi Framework to my project.
- I used PostgreSql and SqlAlchemy to save&read messages.
- OAuth2 is responsible for auth users.
2.Endpoints:
-https://da-plu-2021-jakubszuper.herokuapp.com/Messages -Return a list of all Messages with Id's and number of views.(json format)
- https://da-plu-2021-jakubszuper.herokuapp.com/Create_message - Create a new message and send to database. Endpoint accepts json format for example: 
{"message": "hello world"}. Returning a json {id: id, message: 'message', counter: int}
- https://da-plu-2021-jakubszuper.herokuapp.com/Get_Message/{MessageID} -Return a message with given ID. Also increment number of views(counter).
-  https://da-plu-2021-jakubszuper.herokuapp.com/Update_message -Update message with given id. After update counter should be 0. scheme of payload: 
{"id": "Enter your id","message": "hello world"}. Returning updated message.
-https://da-plu-2021-jakubszuper.herokuapp.com/Message/{MessageID} -Delete the message with given ID. Returning "Deleted the message"
You can check all operations with automatic documentation: https://da-plu-2021-jakubszuper.herokuapp.com/docs. Secured endpoints need auth for the using.(You can choose any login&password to enter)
