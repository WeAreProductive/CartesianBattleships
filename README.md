# Cartesian Battleships DApp

This is the popular Battleships board game suited to run as DApp on the blockchain.
This DApp's back-end is written in Python to run as a [Cartesi rollups](https://cartesi.io/).

## Building the environment

To run the Battleships game server, clone the repository as follows:

```shell
$ git clone https://github.com/WeAreProductive/CartesianBattleships.git
```

Then, build the back-end for the echo example:

```shell
$ cd CartesianBattleships
$ docker buildx bake -f docker-bake.hcl -f docker-bake.override.hcl --load
```

## Running the environment

TODO:

In order to start the containers in production mode, run:

```shell
$ docker-compose -f ./docker-compose.yml -f ./docker-compose.override.yml -f ./docker-compose-host.yml up
```

To stop the containers, first end the process with `Ctrl + C`.
Then, remove the containers and associated volumes by executing:

```shell
$ docker-compose -f ./docker-compose.yml -f ./docker-compose.override.yml -f ./docker-compose-host.yml down -v
```

## Running the environment in host mode

When developing an application, it is often important to easily test and debug it. For that matter, it is possible to run the Cartesi Rollups environment in host mode, so that the DApp's back-end can be executed directly on the host machine, allowing it to be debugged using regular development tools such as an IDE.

The first step is to run the environment in host mode using the following command:

```shell
$ docker-compose -f ./docker-compose.yml -f ./docker-compose.override.yml -f ./docker-compose-host.yml up
```

The next step is to run the game server in your machine. The application is written in Python, so you need to have `python3` installed.

In host mode the game server will work in a Python virtual environment so it must be set up before the first run.
Do this with the following commands:

```shell
$ python3 -m venv .env
$ . .env/bin/activate
$ pip install -r requirements.txt
$ deactivate
```
The first line will create an virtual environment named `.env`.
The second line will enter the newly created virtual environment.
The third line will install the required Python libraries, this is need the first time only.
When inside the virtual environment just type `deactivate` to exit back to the terminal.

Once having the environment setup the Battleship game server can be started with the following command in a dedicated terminal:

```shell
$ . .env/bin/activate
$ ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004" python3 battleships.py
```

After the server successfully starts, it should print an output like the following:

```
[6047] [INFO] Starting gunicorn 19.9.0
[6047] [INFO] Listening at: http://0.0.0.0:5003 (6047)
[6047] [INFO] Using worker: sync
[6049] [INFO] Booting worker with pid: 6049
INFO in log: HTTP dispatcher url is http://127.0.0.1:5004
INFO in log: 
INFO in log: 
INFO in log:      Cartesi                            .) |
INFO in log:    Battleships                       ____|_|_(.
INFO in log:                                      _\______|
INFO in log:                                    _/________|_//_
INFO in log:                _______            /   <<<         |
INFO in log:                \ ...  \___[\\\]__/_________[///]__|___F
INFO in log:    __4__        \                                     |
INFO in log:    \   /         \   V            <<<      <<<        /
INFO in log: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
INFO in log: ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
INFO in log:  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 
INFO in log: 
INFO in log: 
```

When a new game command is sent by client, it should be seen processed by the game server and the game state shown as follows:

```shell
INFO in log: ===== User message (from 0x70997970c51812dc3a010c7d01b50e0d17dc79c8) >>> =====
INFO in log: (Sender/Command/Response) p2: {"gid":"1", "cmd":"m", "arg":{ "shot": [2, 0] } } -> {"gid": "1", "cmd": "m", "arg": {"shot": [2, 0]}, "p": 2}
INFO in log: Game: 1
INFO in log: Turn 3: Player 2 was missed  and shoots at X=2 Y=0
INFO in log: Players 1 and 2 boards:
INFO in log: [~ ~ * ~ ~ ~ ~ ~]    [~ M ~ ~ ~ ~ ~ ~]
INFO in log: [~ ~ ~ ~ ~ ~ ~ ~]    [~ ~ ~ ~ ~ ~ ~ ~]
INFO in log: [~ ~ ~ ~ ~ ~ ~ ~]    [~ ~ ~ ~ ~ ~ ~ ~]
INFO in log: [~ ~ ~ ~ ~ ~ ~ ~]    [~ ~ ~ ~ ~ ~ ~ ~]
INFO in log: [~ ~ ~ ~ ~ ~ ~ ~]    [~ ~ ~ ~ ~ ~ ~ ~]
INFO in log: [~ ~ ~ ~ ~ ~ ~ ~]    [~ ~ ~ ~ ~ ~ ~ ~]
INFO in log: [~ ~ ~ ~ ~ ~ ~ ~]    [~ ~ ~ ~ ~ ~ ~ ~]
INFO in log: [~ ~ ~ ~ ~ ~ ~ ~]    [~ ~ ~ ~ ~ ~ ~ ~]
INFO in log: ===== User message <<< =====
```

The server will run indefinitely untill stopped with `Ctrl+C` or `Ctrl+Z` key combination.

Finally, to stop the containers, removing any associated volumes, execute:

```shell
$ docker-compose -f ./docker-compose.yml -f ./docker-compose.override.yml -f ./docker-compose-host.yml down -v
```

## Running the Battleships game server in Test mode

The game server can be run in TEST mode. This runs and plays a game with predefined moves jsut to show how the gameplay should look at server side. To do so add TEST="1" as environment parameter:

```shell
$ TEST="1" ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004" python3 battleships.py
```
