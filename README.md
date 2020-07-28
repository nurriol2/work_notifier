# Automatic Text Notifications

*Please consider reading [my blog post](https://elliot.bearblog.dev/automatic-text-notifications-project/) to learn more about why I built this program, some explanation about design/organization, and the future improvements.* 

*Thanks!*

# What is this?

This project is my attempt at automating text notifications for my current job.

Every night, my teammates and I recieve a text message with a schedule for the following day. This text is personally sent from our director.

I though that automating this task would be a nice quality of life update for the director and a fun opportunity to use my programming skills for the common good.

# Usage

## Getting the project
1. Clone this repository into a directory using `git clone`
2. `cd /to/project/location`
3. Start a python virtual enviornment:  `python3 -m virtualenv nameOfVirtualEnv`
4. install requirements from `requiremets.txt`

## Your credentials
This project interacts with the Twilio API and the Google Drive API. As such, you will need credentials for both.

For a short explanation of the necessary credentials, see:
`src/credentials_example.py`

*NB:  your `credentials.py` file must be in the same directory as `main.py`*

### Twilio
*This information can be found on your [Twilio Console](https://www.twilio.com/console)*  

After signing up for your Twilio account you will need:
- Account SID
- Authentication Token
- Verified Phone Number
- Twilio Phone Number

### Google Drive
*This information can be found at [this link](https://console.cloud.google.com/)*  

After running `main.py` for the first time, you will be prompted to authorize the app for use with your Google Drive account.

Once authorized, you should
- Check that the Google Drive API is **Enabled**
- Check that the Google Sheets API is **Enabled**
- Download and rename the **Client Secret JSON file**
    - save this in `src/`
- Update the `gsheetId` in your `credentials.py` file

This process needs to be done only once.

## Scheduling the script
Since I have a Unix system, my preferred method for scheduling tasks is using `cron`.  

I have provided the `crontab` for my use case as an example in `example_materials/crontab_example.txt`

# Example Output
The schedule for "tomorrow" might look something like this

![Daily Schedule](https://github.com/nurriol2/work_notifier/blob/master/example_materials/screenshot_02.png)

The header of this table is separated into chronological 15 minute intervals. Employee names are given in Column A and client names fill in the space.

Each employee is responsible for seeing the clients assigned in one row above, below, and equal to where their name appears.

From this portion of the schedule, it looks like everyone starts work at 1:00 pm, except Shaco.
The first clients for Shaco do not appear until 4:30 pm.

The main function of this program would automatically be called by cron at 7:00 pm the day before. Then, the following message would be sent to the specified phone numbers.

![Text Message](https://github.com/nurriol2/work_notifier/blob/master/example_materials/screenshot_01.jpg).

*The keen among you might notice this message was sent after 7:00 pm. This is because I worked on this write-up after.*

# Concepts, Frameworks, and Modules
- Twilio 
- Google Cloud 
- `pandas` module
- `cron`
- Object Oriented Programming
- Python 
