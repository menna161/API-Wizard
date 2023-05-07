from tempfile import NamedTemporaryFile
from typing import IO
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Depends, BackgroundTasks
from pybadges import badge
from pydantic import BaseModel, validator
from keras.models import load_model
from Utils.ImageTools import ImageToArrayPreprocessor
from PrePorcessor.Preprocessor import SimplePreprocessor
from dataset.SimpleDatasetLoader import SimpleDatasetLoader
import cv2
from pymongo import MongoClient
import os
from uvicorn import run
from starlette import status
import shutil
from datetime import datetime
import keras
from fastapi.requests import Request
from fastapi.responses import FileResponse
from fastapi.responses import Response, StreamingResponse
from fastapi.templating import Jinja2Templates


@staticmethod
def get_secure_file_name(file_name: str):
    return f"{datetime.now().timestamp()}.{file_name.split('.')[(- 1)]}"
