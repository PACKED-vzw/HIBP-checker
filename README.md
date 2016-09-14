# HIBP-checker
This script will check a list of email accounts against the API at https://haveibeenpwned.com/API/v2 to see if they are included in a data breach.

If it finds one or more breaches for an account, it will send an email to that account containing a list of leaks the account appeared in, as well as some general information on what to do next (e.g. change passwords). You can customise this message.

To prevent it from sending the same email twice (ccounts do not disappear from breaches), it creates a `.sent` file for every breach it has send an email for (in the `status` directory). If you remove the file, it will send an email again.

It is designed to run automatically without user intervention. All useful information goes to the log file called `log/hibp.log`.

## Installation
Clone the Github repository (or download the tarball and extract it) (in this example, we assume you used `/opt/HIBP-checker` as the location of the script, e.g. by executing `git clone git@github.com:PACKED-vzw/HIBP-checker.git`).

## Configuration
Configuration is done in two places: `config.ini` for application-wide settings and the `accounts` directory to configure which email addresses to query the _haveibeenpwned_ API for.

### `config.ini`
Copy `config/example.ini` to `config/config.ini` and update the following parameters:

* `it_email`: In addition to sending an email to every address it finds in a breach, it will also send one to this email address. This could be one of the addresses of the IT department, so it can get a view of which accounts have been leaked.

* `server`: Your SMTP server (used to send emails).

* `port`: SMTP port. The default is 587.

* `username`: Your SMTP username. Use a full email address (other usernames are not supported), as this will also be the _From_ field in the emails that get sent.

* `password`: SMTP password.

* `msg`: Name of the file in `config` that contains the text of the email message that will be sent to any account found in a leak. There are several `mail._lang_` files (where _lang_ is a ISO-639-1 code - note that this is a convention and not strictly required by the software). You can customise them, but do not remove the `USERNAME` and `LEAKS` tags.

### `accounts`
In the `accounts` directory, create one or more files containing email addresses (one per line) that are to be checked. It doesn't matter what you name the files, but they can only contain email addresses. The application will go through every fail, list all email addresses and query them one by one.

## Usage
It is primarily designed to be used as a cron job. No output is generated to STDOUT, but all messages are instead written in the log file (`log/hibp.log`).

To execute the script, execute `hibp_cron.sh`, preferably as a non-root unprivileged user. No root access is required for the script to function.

### Example cron job
We recommend running it once a week.

```
0 2 * * 1 /opt/HIBP-checker/hibp_cron.sh
```

## License
This software was created by [PACKED vzw](https://github.com/PACKED-vzw/HIBP-checker) and is available under the GPL v3.