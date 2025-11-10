#draws a lottery number betwween min and max across ranges
#public method: draw_numbers
    #does not take any parameters
    # returns a container with n numbers
    # drawn randomly between min and max
#attributes of the lottery: min, max, draw_length
#assumes values have been validated
import random
class Lottery:
    def __init__(self, min=1, max=49, draw_length=6):
        self.__min = min
        self.__max = max
        self.__draw_length = draw_length

    def draw_numbers(self):
        result = []
        while len(result) < self.__draw_length:
            ball = random.randint(self.__min, self.__max)
            if ball not in result:
                result.append(ball)
        return result
      

if __name__ == "__main__":

    lotto649 = Lottery()
    print(lotto649.draw_numbers())
