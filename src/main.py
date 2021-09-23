from play import Play

if __name__ == "__main__":
    play = Play()
    while play.run:
        play.get_events()
