import logging
import os
from datetime import datetime

##Creating logs directory to store log in files
LOG_DIR = "logs"
LOG_DIR = os.path.join(os.getcwd(), LOG_DIR)

##Creating logs directory if not exists
os.makedirs(LOG_DIR, exist_ok=True)

##Creating log file name with current timestamp
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

#Creating log file name with current timestamp
file_name = f"log_{CURRENT_TIME_STAMP}.log"

#Creating log file path for projects
log_file_path = os.path.join(LOG_DIR, file_name)

#Creating log file path for projects
logging.basicConfig(filename=log_file_path,
                    filemode='w',
                    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
                    level=logging.NOTSET)

