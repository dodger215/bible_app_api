from fastapi import FastAPI
from app.router.generator import router as generator_router

app = FastAPI()


app.include_router(generator_router, prefix="/api")






    


