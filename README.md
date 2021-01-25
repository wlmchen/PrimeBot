[![Discord](https://img.shields.io/discord/794255644915007559.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/AtecbFZPZv)
[![License](https://img.shields.io/github/license/pryme-svg/PrimeBot)](https://gitlab.com/pryme-svg/primebot/-/raw/master/LICENSE)
![Code Size](https://img.shields.io/github/languages/code-size/pryme-svg/primebot)
![Total Lines](https://img.shields.io/tokei/lines/github/pryme-svg/primebot)
![Commit Activity](https://img.shields.io/github/commit-activity/y/pryme-svg/primebot?foo=bar)
![Maintained](https://img.shields.io/maintenance/yes/2021)
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

2. Set environment variables

```
heroku config set API_KEY="your_api_key"
heroku config set DISCORD_TOKEN="your_token"
```

3. Push and Run

## Commands

| Command | Aliases | Description |
| ------- | ------- | ----------- |
| `>ping` | N/A | Get the latency of the bot |
| `>quote` | N/A | Get a random quote |
| `>prime` | N/A | Get a description of the developer |
| `>ban (member)` | N/A | Ban a member |
| `>unban (member)` | N/A | Unban a member |
| `>kick (member)` | N/A | Kick a member |
| `>roll` | N/A | Roll a dice |
| `>8ball (question)` | N/A | 8ball |
| `>clear (amount)` | `clean`, `purge` | Delete a number of messages |
| `>poll "question" item1 item2` | N/A | Create a poll |
| `>xkcd` | N/A | Get a random xkcd comic |
| `>xkcd latest` | N/A | Get the latest xkcd comic |
| `>xkcd n (number)` | N/A | Get a specific xkcd comic |
| `>sys` | N/A | Get system information of the host |
| `>info` | N/A | Get information about the bot |
| `>flip` | N/A | Flip a coin |
| `>distro (distro)` | N/A | Get information about a GNU/Linux distribution from distrowatch |
| `>distro random` | N/A | Get information about a random GNU/Linux distro |
| `>apod` | N/A | Get the latest astronomy picture of the day |
| `>apod (date)` | N/A | Get a random apod |
| `>archwiki (term)` | `aw` | Get information from the Arch Wiki |
| `>define (term)` | `df`,  `urbandict`, `ud` | Get definitions from urbandict |
| `>figlet (text)` | `ascii` | Get ascii art |
| `>invite` | N/A | Invite the bot |
| `>b64encode` | `b64e` | Encode text into base64 |
| `>b64decode` | `b64d` | Decode text from base64 |
| `>b16encode` | `b16e` | Encode text into base16 |
| `>b16decode` | `b16d` | Decode text from base16 |
| `>b32encode` | `b32e` | Encode text into base32 |
| `>b32decode` | `b32d` | Decode text from base32 |
| `>b85encode` | `b85e` | Encode text into base85 |
| `>b85decode` | `b85d` | Decode text from base85 |

## Support

Get help at our [discord server](https://discord.gg/AtecbFZPZv)

## Troubleshooting

Create an issue or ask in the discord server with a copy of the `error.log` file

### Licensing

Everything in this repository is licensed under the AGPLv3+ License.
