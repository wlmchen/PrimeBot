[![Discord](https://img.shields.io/discord/794255644915007559.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/AtecbFZPZv)
[![License](https://img.shields.io/github/license/pryme-svg/PrimeBot)](https://gitlab.com/pryme-svg/primebot/-/raw/master/LICENSE)
![PY](https://img.shields.io/badge/--orange?logo=python)

# PrimeBot

A personal bot that runs on Discord.

## Running

1. Retrieve a [nasa api key](https://api.nasa.gov/) and create a `.env` file with the following contents 

```
DISCORD_TOKEN="your_token"
API_KEY="nasa_api_key"
```

2. Run the bot

```
python3 bot.py
```

---

### Deploying to Heroku

1. Create an app

2. Set environemnt variables

```
heroku config set API_KEY="your_api_key"
heroku config set DISCORD_TOKEN="your_token"
```

3. Push and Run

## Support

Get help at our [discord server](https://discord.gg/AtecbFZPZv)

## Troubleshooting

Create an issue or ask in the discord server with a copy of the `error.log` file

### Licensing

Everything in this repository is licensed under the AGPLv3+ License.
