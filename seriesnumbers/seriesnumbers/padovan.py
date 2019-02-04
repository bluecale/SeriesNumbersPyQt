import time


def pad(n,multiply):
    if multiply is None:
        multiply = 1
    seq = []
    for x in range(n):
        if x == 0 or x == 1 or x == 2:
            seq.append(1)
            time.sleep(1)
            yield seq[x]
        else:
            seq.append(seq[x-2] + seq[x-3])
            time.sleep(1)
            yield seq[x]

def draw_padovan(seq):
    import turtle
    pointer = turtle.Turtle()
    pointer.color("white")
    wn = turtle.Screen()
    wn.bgcolor("black")
    pointer.left(90)
    step = 0

    for x in range(len(seq)):
        if step == 0:
            pointer.left(150)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x]) 
            step +=1

        elif step == 1:
            pointer.left(60)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            step += 1

        elif step == 2:
            pointer.left(60)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            step +=1

        elif step == 3:
            pointer.right(120)
            pointer.forward(seq[x])
            pointer.right(120)
            pointer.forward(seq[x])
            step += 1

        elif step == 4:
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            pointer.left(120)
            pointer.forward(seq[x])
            step += 1

        elif step == 5:
            pointer.right(120)
            pointer.forward(seq[x])
            pointer.right(120)
            pointer.forward(seq[x])
            pointer.right(180)
            pointer.forward(seq[x])
            pointer.left(30)
            step = 0


    input()



