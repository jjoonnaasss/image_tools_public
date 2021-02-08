from configparser import ConfigParser

config = ConfigParser()

config.read("config.ini")
config.add_section("main")
config.set("main", "language", "EN")
config.set("main", "suffix", "_processed")

with open("config.ini", "w") as f:
    config.write(f)
