"""
pipeline.py
This file defines full data pipeline VARtigrate data pipeline, mainly using gridstatus API

Integrates functionality of extracting, transforming, and loading data into a SQL database.

Date created: 2025-06-02
Last modified: 2025-06-02
Author: Gordon Doore
"""
from typing import List, Dict, Any
from gridstatus import CAISO
import pandas as pd
import numpy as np 
from fastapi import FastAPI
from database import engine, Base
from routers import users

#code to insert into SQL database


