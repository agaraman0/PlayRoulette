# PlayRoulette

### Rules for playing roulette

- Dealer opens a game
- Multiple players can bet on which number the ball will land
- Dealer closes the game and throws the ball

### Rewards

- Players who bet on the correct number will get double the bet amount as reward
- Other players lose the money to the casino

### Data Points to Track

+ Casino details - Name, BalanceAmount
    - Dealers in a casino - Name
+ User details - Name, BalanceAmount, CurrentCasino
+ Game details - StartTime, EndTime, Status, ThrownNumber
+ Bet details - BetNumber, Amount, BettingTime, User, Game, BetStatus

### Requirements

+ Docker 20.10
+ Postman

## Steps To Run 

```bash
$ git clone git@github.com:agaraman0/PlayRoulette.git

$ cd PlayRoulette

$ touch .env
```

**Update docker-compose.yml with your choice of DB_NAME, DB_USER and DB_PASSWORD like this**

![](https://i.ibb.co/sJCKzk8/Screenshot-from-2021-11-04-10-52-28.png)

**update .env file with same DB_USER, DB_PASSWORD, DB and other environment like this**

![](https://i.ibb.co/YfqGrPm/Screenshot-from-2021-11-04-10-57-58.png)

*Before running this make sure you do not have any existing migration in folder named **migrations/***

```bash
$ docker-compose up -d --build

$ docker ps # you should be able to see 2 docker images running one as application server and another as db server
```

**Our Application is successfully up and running to test it run localhost:5000 in Browser**

To Play Roulette Before That we also have to migrate and populate out DBs for that

```bash
$ docker exec -it <application_server_contianer_name> bash

root@ba6d63/usr/src/app# python manage.py db init

root@ba6d63/usr/src/app# python manage.py db migrate

root@ba6d63/usr/src/app# python manage.py db upgrade
```

Now we are ready to play roulette using apis 


## Play Roulette

### Happy Flow

**Casino Entity**

+ Register Casino
+ Add Multiple Dealers To Registered Casino
+ List All Dealers in a Casino
+ Add/Recharge Amount to Casino Balance

**Dealer Entity**

+ Start Game By A Dealer
  - Dealer Can Only Have One Game Assigned at a time (One to One Relationship between Dealer and Game entity)
  - Dealer Can Start next game only if all other assigned games to dealer are Archived
+ Stop Game By A Dealer
  - Betting on Closed Game not allowed
+ Dealer Throws or Plays Roulette
  - Game can be played once is closed(closed for betting)
  - All Bets are going to settle up here
  - Game Will be archived
  - Dealer Can start next game
  
**User Entity**

+ Register User
+ User Enters in casino
  - User Can Enter into only one casino at one time
  - User Not Bound to only one casino he can switch anytime
+ Add/Recharge Amount to Casino Balance
+ List All Available Open Games in Current casino
+ Make A Bet On available Games in current casino
  - Bet will be settled for a game once dealer throws or plays
  - Casino will get loosing bets amount
  - casino has to pay for user's amount and bet amount will also be added to user balance
+ User will be able to get balance amount


## APIs To Play Roulette

### Casino 

**Entity:**    `/casino/v1`

+ Register casino -> `/create_casino`
+ Add Dealer -> `/:id/add_dealer`
+ List dealers in casino -> `/:id/dealers`
+ Recharge balance -> `/:id/recharge`


### Dealer

**Entity:** `/dealer/v1`

+ Start Game ->    `/:id/start_game`
+ Stop game ->     `/:id/stop_game`
+ Throw ball  -> `/:id/play`
  
### User

**Entity:** `/user/v1`

+ Register -> `/register`
+ Enter casino -> `/:id/enter_casino`
+ Recharge balance -> `/:id/recharge`
+ List of games available for bet -> `/:id/games_available`
+ Bet on game -> `/:id/bet`
+ Cash out -> `/:id/cashout`

**NOTE: to get better understanding about apis use Postman collection**

**Helpful Articles**
+ [Flask Application DB migration](https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/)
+ [Dockerize Flask Application](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/)