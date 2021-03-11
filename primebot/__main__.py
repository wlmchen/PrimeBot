import primebot
import requests_cache

requests_cache.install_cache('requests_cache')  # install requests cache
primebot.PrimeBot().run()
