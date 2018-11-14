# StarLab-APIs

The home of all APIs for the [CredOn](http://credon.kaist.ac.kr/apis) project at [NLP☆CL](http://nlp.kaist.ac.kr).


## Setup

Requires  
`Python 3, MongoDb, flask, flask_mongoengine, requests, ...`.

**Note**  The API modules have their own dependencies; refer to the individual modules for installation details.


## Add new API

To add a new API to this website perform the following three steps.

1. Create an entry in `apis.json` containing some details of the API. Example:

```json
  {
    "api-name": "artext",
    "api-title": "Artext: Artificial Text Generation",
    "description": "Probabilistic Noising of Natural Language"
  }
```

2. Create an view page named `api_<api-name>.html` in the `templates` folder. This is used for accepting input data and displaying results. In addition to text, you can include visual results as per your needs. See `templates/api_artext.html` as reference.


3. Implement two funtions in `app.py`, one for simply rendering the API view page and second for processing the input and returning a `json` reponse. See functions `artext_view()` and `api_artext()` in `app.py` as reference.


## Run

```bash
sudo nohup python3 app.py &
```

