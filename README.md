This project contains a simple distributed cache as a way to experiment with FastAPI.
FastAPI is a new Flask like framework, it brings some advantages like having automatic documentation using Swagger or ReDocs. Also, with FastAPI, we will be using typing to ensure the code has some compile time checks.

Steps to play:

1. Run the appication by `sh ./run_server.sh`
2. Access `http://localhost:8000/docs` and add a remote `http://localhost:8001/pets`
3. Access `http://localhost:8001/docs` and add a new Pet
4. Go back to `http://localhost:8000/docs` and execute the `Sync/Execute` request to fetch the pet added on the other application
5. Profit
6. Show cache.py - we use an OrderedDict to keep track of the recent added items
7. Show distributed.py - using the recent added items, we sync between caches

!(FastAPI Cache Diagram)[FastAPICache.jpg]
!(The Walkthrough)[walk.gif]
