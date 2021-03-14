## Telegram bot for defects management
### API realization is located [here](https://github.com/BogVin/defects-management)
### You can also check out [UI](https://github.com/Chay23/defects-management-react) implemented in React!
***
### How to run?

1. Create **.env** file inside project root folder with environment variables like below:
    TELEGRAM_TOKEN=_your telegram token_  
    BASE_URL=_base api endpoint url_*   
    *You can use url for deployed api: http://defects-management.herokuapp.com/ 

2. Build the docker image:
    ```console
    $ docker-compose build
    ```
3.  Run the container:
    ```console
    $ docker-compose up -d
    ```

