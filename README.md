# LinkedIn Resume Scraper
Automatically download all the resumes from all candidates that have applied to your job on LinkedIn.

This is for educational purposes only. I am not responsible if your LinkedIn account gets suspended or for anything else.

This bot is written in Python using Selenium.

## Setup 

To run the bot, open the command line in the cloned repo directory and install the requirements using pip with the following command:
```bash
pip install -r requirements.txt
```

Next, you need to fill out the config.yaml file. Most of this is self-explanatory but if you need explanations please see the end of this README.

```yaml
email: email@domain.com
password: yourpassword

jobId: 1234567890

disableAntiLock: False

```


## Execute

To run the bot, run the following in the command line:
```
python3 main.py
```

## Config.yaml Explanations

This must be your account that made the job posting.
```yaml
email: email@domain.com
password: yourpassword
```
This is the job id for the job that you made. Go to your job posting and in the URL there should be a number that is around 10 digits long, this is what you need.
```yaml
jobId: 1234567890
```
This prevents your computer from going to sleep so the bot can keep running when you are not using it. Set this to True if you want this disabled.
```yaml
disableAntiLock: False
```
