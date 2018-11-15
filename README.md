# StarLab-APIs

The home of all APIs for the [CredOn](http://credon.kaist.ac.kr/apis) project of [NLP☆CL](http://nlp.kaist.ac.kr).


## Setup

Requires  
`Python 3, MongoDb, flask, flask_mongoengine, ...`.

**Note**  The API modules have their own dependencies; refer to the individual modules for installation details.


## Add new API

To add a new API module to this website perform the following three steps:

1. Create an entry in `apis.json`, containing some details of the API. Example:

```json
  {
    "api-name": "artext",
    "api-title": "Artext: Artificial Text Generation",
    "description": "Probabilistic Noising of Natural Language"
  }
```

2. Create a view page named `api_<api-name>.html` in the `templates` folder. This page has two sections:
   1. A detailed documentation of the API usage.
   2. A live demo of the API, which accepts input data and displays result. Feel free to include graphs and visualizations of the output here.  

   See `templates/api_artext.html` as reference.


3. Implement two funtions in `app.py`, one to render the new API's view page and second to process the input data and return result in `json` format.  

   See the implementations of `artext_view()` and `api_artext()` functions in `app.py` as references.


## Run

```bash
sudo nohup python3 app.py &
```


## Contributors

[Fitsum](http://nlp.kaist.ac.kr/~fgaim), [Seungwon](http://nlp.kaist.ac.kr/~swyoon)
