# RSS Feed Streamer

This project is broken up into three components:

    1. A "worker" that runs continously and fetches RSS feeds from different providers.
    2. A RESTful API that allows you to add rules to filter the RSS feeds with regex and streams the events produced by the worker
    3. A CLI with commands for listing, adding, and deleting rules and a command for streaming the worker output to stdout

## Installation

This project has dependencies on [docker](https://docs.docker.com/get-docker/), [docker-compose](https://docs.docker.com/compose/install/), and [poetry](https://python-poetry.org/docs/#installation). If you have all three of those installed, you can install the project by simply running `make install`. This will run the [docker-compose.yml](./docker-compose.yml) which will build and initiate four services: a postgres database for the API backend, a RESTful API server, a worker that will immediately start fetching RSS feeds, and a [NATS](https://nats.io/) server to act as a message queue. In addition, the `make` target will also run `poetry install` to install the python dependencies for the project.

## Usage

Once everything is installed, activate the python environment by running `poetry shell`. You should now be able to use the `streamrss` CLI command. Here is the output of `streamrss --help`:

```{bash}

Usage: streamrss [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  rules
  stream
```

### Rules

As you can see, there are two subcommands: `stream` and `rules`. The `rules` subcommand has additional subcommands that allow you to `list`, `add`, or `delete` a rule.

```{bash}
Usage: streamrss rules [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add
  delete
  list
```

There are two required parameters for adding a new rule: `--pattern` and `--tag`. The `--pattern` option is for defining the regex that will be ablied to evaluate a feed for a match and the `--tag` option is for giving the rule a name.

```{bash}
Usage: streamrss rules add [OPTIONS]

Options:
  -p, --pattern TEXT  The regex pattern to filter for  [required]
  -t, --tag TEXT      A nametag for the pattern  [required]
  --help              Show this message and exit.
```

Here are some examples:

```{bash}
streamrss rules add --pattern ".*((Ethereum)|(ETH)).*((fork)|(upgrad)).*" --tag "ethereum-forks-or-upgrades"

streamrss rules add --pattern ".*((Coinbase)|(Binance)).*list.*" --tag "coinbase-binance-listings"

streamrss rules add --pattern ".*((hack)|(exploit)|(vuln))" --tag "hack-and-vulnerabilities" 
```

`streamrss rules list` will simply list any existing rules and their corresponding `id`. If you want to delete a rule, you can run `streamrss rules delete --rule-id <ID>` to delete it.

### Stream

Once you have defined some rules, you can start streaming RSS entries by simply running `streamrss stream`. You should see any events that match a defined rule print to stdout.

## API

In addition to the CLI tool, you can interact directly with the API to `GET`/`POST`/`DELETE` rules as well as stream events. The API should be available at `http://localhost:8000/`.

You can view docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

The rules endpoint is: [http://localhost:8000/stream/rules](http://localhost:8000/stream/rules)

And to stream events: [http://localhost:8000/stream](http://localhost:8000/stream)

## Teardown

Lastly, when you are all done, you can tear everything down by running `make destroy` which will bring down all the docker services and remove the docker database volume.
