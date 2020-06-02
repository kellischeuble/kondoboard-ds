import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from .queries import get_all_jobs, search_city_state, search_state, search_all_locations
from .models import Search, Track

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Verifies the API is deployed, and links to the docs
    """
    return HTMLResponse(
        """
    <h1>Kondoboard API</h1>
    <p>Go to <a href="/docs">/docs</a> for documentation.</p>
    """
    )


@app.get("/all")
async def search_all():
    """ 
    Get endpoint to return all jobs
    """
    all = get_all_jobs()
    return all


@app.post("/search/")
async def search_custom(search: Search):
    """
    Endpoint to return custom search when user specifies
    the location and enters in keywords  

    City and state are both optional. However, if a user specifies a city,
    there must also be a state.
    """

    if (search.city == None) and (search.state == None):
        return search_all_locations(search.search)
    elif search.city == None:
        return search_state(search.search, search.state)
    elif search.state == None:
        return {"error":"City must be accompanied by a state"}
    else:
        return search_city_state(search.search, search.city, search.state)

@app.post("/track/")
async def search_by_track(track: Track):
    """ 
    Simple endpoint to return jobs recommended for
    a specific track

    NOTE: will currently return the same jobs as endpoint /all  
    We will be updating this later
    """
    all = get_all_jobs()
    return all
