# ork_cinema

## API Deployment
### Wake up, samurai!
The first thing you have to to is start up the docker containers(by the `docker compose`)
```
docker compose up -d
```
Probably you'll that the API service won't start up, but don't worry. We have no time for making synchronization between starting the API and the Cassandra cluster.
The API will notice that the Cassandra it's not started and just stop because of the
exception.
You have to wait for 10 minutes(yes the fist init takes a long time).
After that you can type the command again.

### Schema init
Obviously(I hope for you too and you are not a "special kid") that now we don't have anything in the DB. So the first thing you have to do to init it is figuring out the name of the API(I've put the init script there). Type the command:
```
docker compose ps
```
Here you must the the row like this:
```
ork_cinema-api-1              ork_cinema-api     "uvicorn main:app --…"   api              19 minutes ago   Up 19 minutes   0.0.0.0:1000->1000/tcp
```
The first string(`ork_cinema-api-1`) is the thing we are looking for.
Then run bash inside the container, you can do it by the command(the name can be different, replace by yours):
```
docker exec -it ork_cinema-api-1 bash
```
Here we go, we are inside. You `pwd` now is in the root of the project(`/app/`).
Now you can init the DB, by the typing
```
python schema_init.py
```
It takes a lot of the time to init DB(Because I'm lazy and don't want to refactor it to the bach approach).
### What's next?
At this step you have started services and initialized the DB. The API must be available at the address `http://127.0.0.1:1000`. Swagger is running at the `http://127.0.0.1:1000/docs`, Redoc at the `http://127.0.0.1:1000/redoc`