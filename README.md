[![Discord](https://img.shields.io/discord/794255644915007559.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/AtecbFZPZv)
[![License](https://img.shields.io/github/license/pryme-svg/PrimeBot)](https://gitlab.com/pryme-svg/primebot/-/raw/master/LICENSE)
![PY](https://img.shields.io/badge/--orange?logo=python)

# PrimeBot

A personal bot that runs on Discord.

## How to Run

1. Install dependencies

`make install_dependencies`

2. Create a `.env` file

In the `.env` file, add the following line, `DISCORD_TOKEN="YOUR_TOKEN"`

For apod functionality, retrieve an API key [here](https://api.nasa.gov/) and add the following line.

`API_KEY="YOUR API KEY"`

3. Run the bot

`python bot.py`

---

Alternatively, create a systemd service using `primebot.service.example`:

```
[Unit]
Description=PrimeBot
After=syslog.target
After=network.target

[Service]
RestartSec=2s
Type=simple
User=primebot
Group=primebot
WorkingDirectory=/home/primebot/PrimeBot
ExecStart=python3 /home/primebot/PrimeBot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Copy the file to `/etc/system/systemd/primebot.service`

Start the service 

`# systemctl start primebot.service`

Autostart with 

`# systemctl enable primebot.service`

## Support

Get help at our discord server: `https://discord.gg/AtecbFZPZv`

## Troubleshooting

Create an issue or ask in the discord server with a copy of the `error.log` file

### Licensing

Everything is licensed under the AGPLv3+ License.
