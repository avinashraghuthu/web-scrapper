Pre-requisites:
    Install the pre-requisites by following command:
        pip install -r requirements.txt


Running the setup:
    Run the following command to run the server:
        ./manage.py runserver 0.0.0.0:8000

        where last argument specify the Ip and port on which we want to run



APIS:

 1) URL : http://[IP]:[PORT]/scrapper/v1/webscrapper/

    METHOD: POST

    PARAMETERS: web_url
                    - url from which you want to extract the h1 and h2 tags

    Sample Url : http://127.0.0.1:8000/scrapper/v1/webscrapper/


 2) URL : http://[IP]:[PORT]/scrapper/v1/webscrapper/

    METHOD: GET

    PARAMETERS: offset
                    - Gives the starting point of the pagination list,
                limit
                    - Specifies the endning point of the pagination list

    Sample Url: http://127.0.0.1:8000/scrapper/v1/webscrapper/?limit=10&offset=0
