# fyda - The "interface For Your DAta"

This package is still under construction. Below is a build plan for expected
features.


## Features

Easily interact with your data using as little python code as possible. Control
the available data in the ``input`` folder, and use fyda's built-in api to
load it, transform it, and model it. 


## User guide

You should [Read The Docs](https://fyda.readthedocs.io/en/latest/) for all
the goodies!


## Installation

Currently the only way to get fyda is by installing it manually from github.
fyda is developed with the Anaconda distribution virtual environment
achitecture in mind but you can use whatever venv setup you like.
Assuming your current working directory is where you want to put this repo, 

```sh
git clone https://github.com/renzmann/fyda
```


Next, install the requirements

(Linux / macOS)

```sh
$ while read requirement; do conda install --yes $requirement; done < requirements.txt
```

(Windows)

```sh
> FOR /F "delims=~" %f in (requirements.txt) DO conda install --yes "%f" || pip install "%f"
```

Finally, install fyda

```sh
pip install .
```


