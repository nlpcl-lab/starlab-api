# StarLab-APIs

The home of all APIs for the [CredOn](http://credon.kaist.ac.kr/apis) project of [NLP☆CL](http://nlp.kaist.ac.kr).

## Dependencies

Requires **Python 3** or higher.

- flask
- flask_mongoengine
- other modules for API...

> **Note**: The API modules have their own dependencies; refer to the individual modules for installation details.

## Setup

1. Install `mongoDB`, and set environments for it at your server.
2. Install the necessary modules with `pip install -r requirements.txt` command. You can add any modules if you needed to.
3. Open `config.sample.py`. Rewrite the information in the file, and rename it as `config.py`.

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

3) Implement two funtions in `app.py`, one to render the new API's view page and second to process the input data and return result in `json` format.

   See the implementations of `artext_view()` and `api_artext()` functions in `app.py` as references.

## Run Service

To run the service in background, `cd` to `starlab-api` folder and execute the following command:

```bash
sudo nohup python app.py >> log.txt 2>&1 &
echo $! > pid.txt
```

The site should be accessible at `http://<host-ip>:8084`.  
Check `log.txt` if there are any problems.

# Stop Service

To kill the service started above, execute the following command inside the `starlab-api` folder:

```bash
sudo kill -9 `cat pid.txt`
```

## Contributors

[Fitsum](http://nlp.kaist.ac.kr/~fgaim), [Seungwon](http://nlp.kaist.ac.kr/~swyoon), [Junseop](https://github.com/gaonnr)
