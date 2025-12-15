import schedule
import time
import logging
import subprocess
from datetime import datetime

logger = logging.getLogger(__name__)

def run_collection():
    today = datetime.now().weekday()
    # Mon=0, Tue=1, Wed=2
    if today <= 2: 
        logger.info("Scheduler: Starting Collection Job")
        subprocess.run(["python", "main.py", "--mode", "collect"])
    else:
        logger.info("Scheduler: Skipping collection (not Mon-Wed)")

def run_report():
    today = datetime.now().weekday()
    # Fri=4
    if today == 4:
        logger.info("Scheduler: Starting Reporting Job")
        subprocess.run(["python", "main.py", "--mode", "summarize"])
    else:
        logger.info("Scheduler: Skipping report (not Friday)")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Scheduler started...")
    
    # Schedule collection for Mon-Wed mornings
    schedule.every().day.at("08:00").do(run_collection)
    
    # Schedule report for Friday afternoon
    schedule.every().friday.at("16:00").do(run_report)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
