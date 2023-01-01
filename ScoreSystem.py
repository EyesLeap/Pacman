class ScoreSystem:

    def __init__(self):
        self.high_score = 0


    def recordHighScore(self, score):
        if score > self.high_score:
            self.high_score = score
            with open("HighScore.txt", "w") as file:
                file.write(str(self.high_score))


    def loadHighScore(self):
        with open("HighScore.txt", "r") as file:
            #print(file.readline())
            self.high_score = file.readline()
            self.high_score = int(self.high_score)

        return self.high_score
