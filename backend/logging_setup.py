import logging

def setup_logger(name):
    logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  
    filemode='a'      
    )
    return logging.getLogger(name)