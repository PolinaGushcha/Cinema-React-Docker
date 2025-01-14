import logging

from cassandra.cluster import Cluster
from config import CassandraConfig
from db.cassandra import CassandraPool
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.cinemas import router as cinemas_router
from routers.debug import router as debug_router
from routers.seats import router as seats_router
from routers.users import router as users_router

logger = logging.getLogger(__name__)

app = FastAPI()


app.include_router(debug_router)
app.include_router(seats_router)
app.include_router(cinemas_router)
app.include_router(users_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Initializing the cassandra pool...")
    cassandra_config = CassandraConfig.get_config()
    logger.info(f"Using cassandra host: {cassandra_config.HOST}")
    app.state.cassandra_pool = CassandraPool(
        Cluster(cassandra_config.HOST),
        4,
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
