## Installation

This instruction assumes that you will be running the application in a Linux environment.

Clone this repository then move to the `master` branch.

Requires Python3.8 or above.

Create virtual environment then install the packages from the requirements file.

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

Install redis.

Follow the instructions from the official website.

[Redis Installation](https://redis.io/docs/getting-started/installation/install-redis-on-linux/)

Keep the default settings

Activate redis server on another terminal window.

```bash
redis-server
```

## Required file
Create a .env file on the root directory with the following data:

```bash
JWT_SECRET=<Supply text here>
JWT_ALGORITHM=HS256
SENDGRID_API_KEY=<enter sendgrid api>
FROM_EMAIL=<source email registered in sendgrid>


```

## Usage

Run command below to start development server.

```bash
python main.py
```
