import time


def Fib(n, off, multiply):
    """
    generator that yields the numbers in the fibonacci series

    :param n: number of numbers to yield
    :param offset: offset from the first number
    :param multiply: multiply the whole sequence by 
    :type n, offset, multiply: int
    """
    a = 0
    b = 1
    for i in range(n + off):
        a, b = b, a+b
        if i > off - 1:
            time.sleep(0.5)
            yield a*multiply
        

def drawFibonacci(seq, pen_color, background_color):
    """
    displays the series with TurtleGraphics

    :param seq: the series of numbers to rapresent
    :type seq: list[int]

    :param pen_color, background_color: the colors expressed in hex selected with the picker
    :type pen_color, bakground_color: str
    """
    import turtle
    pointer = turtle.Turtle()
    pointer.color(pen_color)
    wn = turtle.Screen()
    wn.bgcolor(background_color)

    for x in range(6):
        pointer.left(90)
        pointer.forward(seq[0])

    for n in range(len(seq)-1):
        pointer.speed(5)
        pointer.left(90)
        pointer.forward(seq[n+1] + seq[n])
        pointer.left(90)
        pointer.forward(seq[n+1])
        pointer.left(90)
        pointer.forward(seq[n+1] + seq[n]) 
    input()