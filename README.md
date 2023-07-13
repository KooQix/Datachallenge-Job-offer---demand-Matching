# Description

_Hackathon proposed by my Engineering School (French), in partnership with a company nearby, when I was in second year. The goal was to match a job offer with the best profiles. Low energy consumption was one of the requirements, therefore we could not use use a deep neural network._

I used web scraping to get the qualities required by a job and then regrouped the jobs in the database using a clustering method (KMeans).

Categories were created, for example distance to the job, given the information about the job offer and a profile. Each category has a percentage of match, using its own distance measurement.
Each category also has a weight, adjustable in the configuration file.

For a given offer, the program goes through each profile and gives a percentage of match for each category, and then a global percentage, as a weighted average.

Then, the program sorts the results by decreasing percentages and returns the first n profiles.

It works the same for a given profile, looking to get the best offers.

> API in Python, using FastAPI.\
> Check out the requests.http file to get an idea of the available HTTP endpoints and the json files in response-examples to get an idea of the responses.

**Our team won this DataChallenge!** See LinkedIn post: https://www.linkedin.com/posts/ia-pau_les-r%C3%A9sultats-sont-tomb%C3%A9s-ca-y-est-activity-6917026474390671360-GkE0?utm_source=share&utm_medium=member_desktop

### Requirements

-   Conda needs to be installed:

        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
        chmod +x Miniconda3-latest-Linux-x86_64.sh
        bash Miniconda3-latest-Linux-x86_64.sh -p $HOME/miniconda3

        conda create -n venv python=3.10
        cd path/to/project
        pip3 uninstall uvicorn
        conda activate venv

        pip3 install "fastapi[all]" PyMySQL nltk unidecode spacy geopy sklearn pandas python-dotenv cryptography joblib sqlalchemy

        rm -r path/to/miniconda3/envs/venv/lib/python3.10/site-packages/click
        cp -r ./resources/click path/to/miniconda3/envs/venv/lib/python3.10/site-packages/
        python3 -m spacy download fr_core_news_md

-   NodeJS installation & required dependencies

        sudo apt install nodejs npm chromium -y

        python3 ./models/gen/nltk_download.py
        cd ./services/web && npm install

## Get started

-   rename .env-example to .env & set up your credentials

#### Generate database

-   Create your MySQL database

-   Set .env: DB_NAME accordingly

#### Fill in the database (might takes some time, due to the web scraping)

    python3 models/gen/populateDB.py

or (inside mysql)

    source path/to/project/models/gen/DB_TEDDY_WINNERS.sql

## Start App (python environment needs to be activated)

    uvicorn main:app

##### Possible errors encountered

_If you get an error like: "match_info: list[dict[str, int]] type is not subscriptable", you may need to uninstall your global uvicorn (if using a virtual environment)._\
_To do so, deactivate your python environnement and run pip3 uninstall uvicorn. Reactivate your environment and try running uvicorn main:app again_

##### Notes

_Profiles have been anonymized_
