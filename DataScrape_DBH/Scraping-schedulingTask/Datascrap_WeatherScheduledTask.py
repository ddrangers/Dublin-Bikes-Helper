# In Jupyter notebook, every time a cell is executed,
# a new Python interpreter process is created,
# which may cause the timing task to fail.
# In addition, Jupyter notebook itself not being able to run tasks in the background.
# So,I upload a py file.



import schedule
import time


def get_weather():
    print('this is the scraping data process!!!')


def run_task():
    # Set daily scheduled tasks.
    schedule.every().day.at("08:00").do(get_weather)

    # Infinite loop, automatically run scheduled tasks in the background
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start a scheduled task
run_task()