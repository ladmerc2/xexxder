## Sennder Task

#### Getting Started

  - clone project locally
  - Make sure to have docker and docker-compose installed
  - RUN `make` or RUN `docker-compose up` in project root
  - A `.env` is auto-generated on project build just to avoid you manually creating an env file yourself for "this test"
  - When project is done building head over to http://localhost:8000/movies/

#### Test
  - RUN `make test` this also shows coverage report
  - To view coverage report in html RUN `coverage html` this would add a `htmlcov` folder to the root project, head over to the index.html and open that in browser

#### Lint Check
  - RUN `make lint` , coding style guide -PEP8, black for formatting

## Notes

  #### Optimization

    - On first page load, response takes about 10secs
    - But on second load redis caches for 60s
    - Code space/time complexity is O(n)T, O(n)S
    - Other helpful feature would have been pagination.

  ### Can improve
  
    - One first page load, should display the page then add a loader instead of nothing showing up first
    - Makefile has repeated copy to generate env for each target, it can be done better