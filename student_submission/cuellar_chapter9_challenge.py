
class Game:
    def __init__(self):
        self.frames = []


class Frame:
    def __init__(self):
        self.rolls = []

    def add_roll(self, pins):
        self.rolls.append(pins)

    def is_strike(self):
        return self.rolls[0] == 10

    def is_spare(self):
        return sum(self.rolls) == 10 and len(self.rolls) == 2


class BowlingGame(Game):
    def __init__(self):
        super().__init__()

    def score(self):
        rolls = []

        for frame in self.frames:
            rolls.extend(frame.rolls)

        total = 0
        roll_index = 0

        for frame_number in range(10):
            if rolls[roll_index] == 10:
                total += 10 + rolls[roll_index + 1] + rolls[roll_index + 2]
                roll_index += 1

            elif rolls[roll_index] + rolls[roll_index + 1] == 10:
                total += 10 + rolls[roll_index + 2]
                roll_index += 2

            else:
                total += rolls[roll_index] + rolls[roll_index + 1]
                roll_index += 2

        return total


game = BowlingGame()

for frame_number in range(1, 11):
    print(f"\nFrame {frame_number}:")
    frame = Frame()

    first_roll = int(input("How many pins did you knock down? "))
    frame.add_roll(first_roll)

    if frame_number < 10:
        if first_roll == 10:
            print("Strike!")

        else:
            second_roll = int(input("How many pins on your second roll? "))
            frame.add_roll(second_roll)

            if first_roll + second_roll == 10:
                print("Spare!")

    else:
        if first_roll == 10:
            print("Strike!")
            second_roll = int(input("Bonus roll 1: "))
            frame.add_roll(second_roll)

            third_roll = int(input("Bonus roll 2: "))
            frame.add_roll(third_roll)

        else:
            second_roll = int(input("How many pins on your second roll? "))
            frame.add_roll(second_roll)

            if first_roll + second_roll == 10:
                print("Spare!")
                bonus_roll = int(input("Bonus roll: "))
                frame.add_roll(bonus_roll)

    game.frames.append(frame)

    print("Frames completed:", len(game.frames))


print("\nYour final score is:", game.score())











