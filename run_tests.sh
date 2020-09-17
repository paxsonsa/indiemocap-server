#! /bin/bash
export PYTHONPATH="src/"
pytest --cov=indiemocap tests/
