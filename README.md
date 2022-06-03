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
$ make machine
```

## Running the environment

In order to start the containers in production mode, simply run:

```shell
$ docker-compose up --build
```

_Note:_ If you decide to use [Docker Compose V2](https://docs.docker.com/compose/cli-command/), make sure you set the [compatibility flag](https://docs.docker.com/compose/cli-command-compatibility/) when executing the command (e.g., `docker compose --compatibility up`).

Allow some time for the infrastructure to be ready.
How much will depend on your system, but after some time showing the error `"concurrent call in session"`, eventually the container logs will repeatedly show the following:

```shell
server_manager_1      | Received GetVersion
server_manager_1      | Received GetStatus
server_manager_1      |   default_rollups_id
server_manager_1      | Received GetSessionStatus for session default_rollups_id
server_manager_1      |   0
server_manager_1      | Received GetEpochStatus for session default_rollups_id epoch 0
```

To stop the containers, first end the process with `Ctrl + C`.
Then, remove the containers and associated volumes by executing:

```shell
$ docker-compose down -v
```

## Running the environment in host mode

When developing an application, it is often important to easily test and debug it. For that matter, it is possible to run the Cartesi Rollups environment in [host mode](../README.md#host-mode), so that the DApp's back-end can be executed directly on the host machine, allowing it to be debugged using regular development tools such as an IDE.

The first step is to run the environment in host mode using the following command:

```shell
$ docker-compose -f docker-compose.yml -f docker-compose-host.yml up --build
```

The next step is to run the game server in your machine. The application is written in Python, so you need to have `python3` installed.

In order to start the game server, run the following commands in a dedicated terminal:

```shell
$ cd CartesianBattleships/server/
$ python3 -m venv .env
$ . .env/bin/activate
$ pip install -r requirements.txt
$ HTTP_DISPATCHER_URL="http://127.0.0.1:5004" gunicorn --reload --workers 1 --bind 0.0.0.0:5003 gameserver:app
```

This will run the game server on port `5003` and send the corresponding notices to port `5004`. The server will also automatically reload if there is a change in the source code, enabling fast development iterations.

The final command, which effectively starts the server, can also be configured in an IDE to allow interactive debugging using features like breakpoints. In that case, it may be interesting to add the parameter `--timeout 0` to gunicorn, to avoid having it time out when the debugger stops at a breakpoint.

After the server successfully starts, it should print an output like the following:

```
[2022-06-03 15:18:43 +0300] [6047] [INFO] Starting gunicorn 19.9.0
[2022-06-03 15:18:43 +0300] [6047] [INFO] Listening at: http://0.0.0.0:5003 (6047)
[2022-06-03 15:18:43 +0300] [6047] [INFO] Using worker: sync
/usr/lib/python3.8/os.py:1023: RuntimeWarning: line buffering (buffering=1) isn't supported in binary mode, the default buffer size will be used
  return io.open(fd, *args, **kwargs)
[2022-06-03 15:18:43 +0300] [6049] [INFO] Booting worker with pid: 6049
[2022-06-03 15:18:44,147] INFO in log: HTTP dispatcher url is http://127.0.0.1:5004
[2022-06-03 15:18:44,148] INFO in log: 
[2022-06-03 15:18:44,148] INFO in log: 
[2022-06-03 15:18:44,148] INFO in log:      Cartesi                            .) |
[2022-06-03 15:18:44,148] INFO in log:    Battleships                       ____|_|_(.
[2022-06-03 15:18:44,148] INFO in log:                                      _\______|
[2022-06-03 15:18:44,148] INFO in log:                                    _/________|_//_
[2022-06-03 15:18:44,148] INFO in log:                _______            /   <<<         |
[2022-06-03 15:18:44,148] INFO in log:                \ ...  \___[\\\]__/_________[///]__|___F
[2022-06-03 15:18:44,148] INFO in log:    __4__        \                                     |
[2022-06-03 15:18:44,149] INFO in log:    \   /         \   V            <<<      <<<        /
[2022-06-03 15:18:44,149] INFO in log: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[2022-06-03 15:18:44,149] INFO in log: ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
[2022-06-03 15:18:44,149] INFO in log:  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 
[2022-06-03 15:18:44,149] INFO in log: 
[2022-06-03 15:18:44,149] INFO in log: 
^C[2022-06-03 15:18:46 +0300] [6047] [INFO] Handling signal: int
[2022-06-03 15:18:46 +0300] [6049] [INFO] Worker exiting (pid: 6049)
[2022-06-03 15:18:46 +0300] [6047] [INFO] Shutting down: Master

```

After that, you can interact with the application

When you add an input, you should see it being processed by the game server as follows:

```shell
[2022-01-21 15:58:39,555] INFO in echo: Received advance request body {'metadata': {'msg_sender': '0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266', 'epoch_index': 0, 'input_index': 0, 'block_number': 11, 'time_stamp': 1642791522}, 'payload': '0x636172746573690d0a'}
[2022-01-21 15:58:39,556] INFO in echo: Adding notice
[2022-01-21 15:58:39,650] INFO in echo: Received notice status 201 body b'{"index":0}'
[2022-01-21 15:58:39,651] INFO in echo: Finishing
[2022-01-21 15:58:39,666] INFO in echo: Received finish status 202
```

The game server can be run in TEST mode. This runs and plays a game with predefined moves jsut to show how the gameplay should look at server side. To do so add TEST="1" as environment parameter:

```shell
$ TEST="1" HTTP_DISPATCHER_URL="http://127.0.0.1:5004" gunicorn --reload --workers 1 --bind 0.0.0.0:5003 gameserver:app
```

Finally, to stop the containers, removing any associated volumes, execute:

```shell
$ docker-compose -f docker-compose.yml -f docker-compose-host.yml down -v
```
