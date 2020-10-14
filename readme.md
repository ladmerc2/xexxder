## Sennder Task

#### Getting Started

  - clone :)
  - Make sure to have docker and docker-compose installed
  - RUN `make` or RUN `docker-compose up`
  - When project is done building head over to http://localhost:8000/movies/

#### Test
  - RUN `make test` this also shows coverage report

#### Lint Check
  - RUN `make lint`

## Notes

 #### Optimization

    - On first page load, response takes about 10secs
    - But on second load redis caches for 60s
    - Code space/time complexity is O(n)T, O(n)S
    - Other helpful feature would have been pagination.
