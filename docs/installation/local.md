# Local Development Setup

The instructions on this page will guide you in setting up a local development environment in your system. Query-Server needs Python 2 to run. Most of the distros come bundled with that but if it is not there please install it first.

## Steps

* **Step 0** - For a start, fork Query-Server to your own github account. Then, clone it to your local system.

```sh
$ git clone -b master https://github.com/<your_username>/query-server.git
```

Add an upstream remote so that you can push your patched branches for starting a PR .

```sh
$ cd query-server
$ git remote add upstream https://github.com/fossasia/query-server.git
```

* **Step 1** - Make sure you have [Nodejs](https://nodejs.org/en/) installed. Running this tool requires installing the nodejs as well as python dependencies.

* Now in the terminal in query-server directory, run the following commands

```sh
$ npm install -g bower
$ bower install
$ pip install virtualenv
$ virtualenv venv
```
* Now to activate the virtual environment, type this:

*For Linux users*
```sh
$ . venv/bin/activate
```
*For Windows users*
```sh
venv\Scripts\activate
```
* Now to install the requirements, type

```sh
$ pip install -r requirements.txt
```


If you want to use [`pipenv`](https://docs.pipenv.org) instead of using `pip` and `virtualenv` separately, do the following:

```sh
$ npm install -g bower
$ bower install
$ pip install pipenv
$ pipenv --two # To setup python 2 virtual environment
$ pipenv install -r requirements.txt
$ pipenv shell # To activate virtual environment
```

* **Step 2** - Now you need to set up MongoDB on your server. For this, follow these steps :

```sh
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
$ echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
$ sudo service mongod start
```

* **Step 3** - To run the project on a local machine.

* For development mode (with debugger active), use the following command
```sh
$ python app/server.py --dev
```

* To run the project on a production machine.
```sh
$ python app/server.py
```

## Preferred Development Workflow

1. Get the latest copy of code from upstream.

```sh
$ git pull upstream master
```

2. Once you get assigned an issue, create a new branch from `master`.

```sh
$ git checkout -b XXX-mock-issue     # XXX is the issue number
```

3. Work on your patch, test it and when it's done, push it to your fork.

```sh
$ git push origin XXX-mock-issue
```

4. File a PR and wait for the maintainers to suggest reviews or in the best case merge the PR. Then just update `master` of your local clone.

```sh
$ git pull upstream master
```

And then loop back again. For contribution guidelines, refer [here](https://github.com/fossasia/query-server/blob/master/.github/CONTRIBUTING.md).
