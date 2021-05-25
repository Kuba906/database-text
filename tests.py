from fastapi.testclient import TestClient

import main

client = TestClient(main.app)

async def test_get_message():
    
    response = await client.get('/Messages')
    assert response.status_code ==200

async def test_get_message():
    
    response = await client.get('/Messages')
    assert response.status_code ==200

async def test_get_messages(response_model=main.List[main.MessagesList]):
    query=main.messages.select()

    response = await client.get('/Messages')
    assert response.status_code ==200

async def test_get_message(response_model = main.MessagesList):
    response = await client.get("/Get_Message/{MessageID}")
    query = main.messages.update().\
        where( main.messages.c.id == main.messages).\
            values(
                counter =  main.messages.c.counter +1
            )
    await main.database.execute(query)
    assert response.status_code ==200
