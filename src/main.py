from states.play import Play

if __name__ == "__main__":
    play = Play()
    while play.run:
        play.state_events()
