#!/bin/bash

cp -r /seed/models/* /app/models/ && cp -r /seed/data/* /app/data/ && cp -r /seed/mlruns/* /app/mlruns/
echo "Initial data, models, and mlruns have been copied."
