# Local Development Setup

The instructions on this page will guide you in setting up a local development environment in your system.

For a start, fork Query-Server to your own github account. Then, clone it to your local system.

```sh
git clone -b master https://github.com/<your_username>/query-server.git
```

Add an upstream remote so that you can push your patched branches for starting a PR .

```sh
cd query-server
git remote add upstream https://github.com/fossasia/query-server.git
```

Make sure you have [Nodejs](https://nodejs.org/en/) installed.
Running this tool requires installing the nodejs as well as python dependencies.

```
npm install -g bower
bower install
pip install virtualenv
virtualenv venv
. venv/bin/activate # Linux
venv\Scripts\activate # Windows
pip install -r requirements.txt
```

or to use [`pipenv`](https://docs.pipenv.org) instead of `pip` and `virtualenv` separately.

```
npm install -g bower
bower install
pip install pipenv
pipenv --two # To setup python 2 virtual environment
pipenv install -r requirements.txt
pipenv shell # To activate virtual environment
```

To set up MongoDB on your server on ubuntu machine :

```bash
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
sudo apt-get install -y mongodb
sudo service mongod start
```

To set up MongoDB on your server on mac machine :

```
brew install mongo
sudo mkdir -p /data/db
whoami
sudo chown <output_of_whoami> /data/db
export MONGO_PATH=<path_to_mongodb>
export PATH=$PATH:$MONGO_PATH/bin
mongod
```

To run the project on a local machine.

For development mode (with debugger active), use the following command
```sh
python app/server.py --dev
```

To run the project on a production machine.

```sh
python app/server.py
```

## Preferred Development Workflow

1. Get the latest copy of code from upstream.

```sh
git pull upstream master
```

2. Once you get assigned an issue, create a new branch from `master`.

```sh
git checkout -b XXX-mock-issue     # XXX is the issue number
```

3. Work on your patch, test it and when it's done, push it to your fork.

```sh
git push origin XXX-mock-issue
```

4. File a PR and wait for the maintainers to suggest reviews or in the best case
merge the PR. Then just update `master` of your local clone.

```sh
git pull upstream master
```

And then loop back again. For contribution guidelines, refer [here](https://github.com/fossasia/query-server/blob/master/.github/CONTRIBUTING.md)
