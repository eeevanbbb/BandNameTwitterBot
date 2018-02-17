# Band Name Twitter Bot

## Requirements

- `python 2.7`
- TwitterBot credentials

## Installation

`pip install -r Requirements.txt`

## Usage
usage: Main.py [-h] [--twitter TWITTER_FILE] [--source SOURCE]

Run the bot.

optional arguments:
  -h, --help            show this help message and exit
  --twitter TWITTER_FILE
                        The file containing the Twitter keys, one per line
                        with the format key_name=key_value (default:
                        twitter_config.txt)
  --source SOURCE       The URL from which to request band names (default:
                        https://bots-176817.appspot.com/band_name)

## Source

The band names come from a markov chain based on band names contributed to a private Facebook.com group that you cannot join.

But you can get as many of the band names as you like here: http://bands.evanb.io

## Credit

Credit goes to the hundreds of people who have contributed band names to the Facebook.com group that was used to train this bot. Thanks! You have been replaced!