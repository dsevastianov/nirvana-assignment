# Aggregator API

Simple API that coallesces calls from multiple upstream APIs with the same contract.

This project relies on docker compose to run required services. Run `docker-compose up` in the root of the project and open `http://localhost:5000/member_id=1&strategy=max` in your browser to see Aggregator API in action.
To run unit tests: `pytest --cov-report html --cov aggregator`.

## Possible further improvements
- Move to production server
- Build dev vs prod configuration
- Move strategy into separate endpoint
