from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI
from controllers import client, jober, job
from os import environ
app = FastAPI()



	#################### Enable CORS ####################
 
origins = ['*']  # Default, all origins. Edit this array to customize your origins. 

# If origins != *, set allow_credentials=True below
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




	#################### Add routers ####################
 
app.include_router(router=client.router, prefix="/api/client")
app.include_router(router=jober.router, prefix="/api/jober")
app.include_router(router=job.router, prefix="/api/job")




if (__name__ == '__main__'):
    uvicorn.run("main:app", port=environ.get('API_PORT'))