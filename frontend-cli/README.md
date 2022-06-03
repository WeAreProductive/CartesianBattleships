# Cartesian Battleships CLI client

This is a front-end client for the Cartesian Battleships game.
This client is written in Node.js, it has Text UI and runs in a console.

## Building and starting the CLI client

```bash
$ npm run build2
$ npm run start
```

## Playing game with the CLI client

After starting the client will prompt to user to select a predefined hardhat wallet to use to play the game.

```bash
? Select player (Use arrow keys)
❯ Player 1 
  Player 2 
```

After a wallet is selected the main game menu will be shown.

```

         Cartesi                            .) |                    
       Battleships                       ____|_|_(.                 
                                         _\______|                  
                                       _/________|_//_              
                   _______            /   <<<         |             
                   \ ...  \___[\\\]__/_________[///]__|___F         
       __4__        \                                     |         
       \   /         \   V            <<<      <<<        /         
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     
    ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~     
     ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~      
                                                                    
                                                                    
    ────────────────────────────────────────────────────────────    
    Create game                                                     
    Join game                                                       
    ────────────────────────────────────────────────────────────    
    Exit                                                            

```

## Creating new game

## Joining a game

## Playing a game

Use arrow keys to move cursor on opponent's board and Enter to shoot at selected coordinates.

```
  ╔═════════════════════════════════════════════════════════════════╗ ┌─────────────────────┐
  ║  Game ID: 1                                                     ║ │   1. P1: C4 miss    │
  ║ Player 1: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 (me)       ║ │   2. P2: D5 miss    │
  ║ Player 2: 0x70997970C51812dc3A010C7d01b50e0d17dc79C8            ║ │   3. P1: D3 HIT     │
  ╚═════════════════════════════════════════════════════════════════╝ │   4. P2: E6 HIT     │
                                                                      │   5. P1: B5 HIT     │
     Opponent's fleet                    My fleet                     │   6. P2: E3         │
      A B C D E F G H I J K L             A B C D E F G H I J K L     │                     │
   1 [O ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]         1 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]    │                     │
   2 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]         2 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]    │                     │
   3 [~ M ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]         3 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]    │                     │
   4 [~ ~ X ~ ~ ~ ~ ~ ~ ~ ~ ~]         4 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]    │                     │
   5 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]         5 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]    │                     │
   6 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]         6 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]    │                     │
   7 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]         7 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]    │                     │
   8 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]         8 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]    │                     │
   9 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]         9 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]    │                     │
  10 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]        10 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]    │                     │
  11 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]        11 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]    │                     │
  12 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]        12 [~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~]    │                     │
      A1                                                              └─────────────────────┘

  My turn. User arrow keys to move, Enter to shoot.

```
