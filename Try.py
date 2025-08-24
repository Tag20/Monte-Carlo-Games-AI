import turtle
import random
import time

def Pong():
    win = turtle.Screen()
    win.title("Pong with MCTS AI")
    win.bgcolor("black")
    win.setup(width=800, height=600)
    win.tracer(0)

    score_1 = 0
    score_2 = 0

    paddle_1 = turtle.Turtle()
    paddle_1.speed(0)
    paddle_1.shape("square")
    paddle_1.color("white")
    paddle_1.shapesize(stretch_wid=5, stretch_len=1)
    paddle_1.penup()
    paddle_1.goto(-350, 0)

    paddle_2 = turtle.Turtle()
    paddle_2.speed(0)
    paddle_2.shape("square")
    paddle_2.color("white")
    paddle_2.shapesize(stretch_wid=5, stretch_len=1)
    paddle_2.penup()
    paddle_2.goto(350, 0)

    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("square")
    ball.color("white")
    ball.penup()
    ball.goto(0, 0)
    ball.dx = 0.7  # Increased speed
    ball.dy = 0.7  # Increased speed

    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 260)
    pen.write("Player A: 0 MCTS AI: 0", align="center", font=("Courier", 24, "normal"))

    def paddle_1_up():
        if paddle_1.ycor() < 250:
            paddle_1.sety(paddle_1.ycor() + 40)  # Faster movement

    def paddle_1_down():
        if paddle_1.ycor() > -250:
            paddle_1.sety(paddle_1.ycor() - 40)  # Faster movement

    def ai_move():
        """MCTS-based AI move selection."""
        best_move = 0
        best_score = float('-inf')
        actions = [0, 40, -40]  # Faster movement
        
        for action in actions:
            new_y = paddle_2.ycor() + action
            if -250 <= new_y <= 250:
                reward = mcts_simulate(new_y)
                if reward > best_score:
                    best_score = reward
                    best_move = action
        
        paddle_2.sety(paddle_2.ycor() + best_move)
    
    def mcts_simulate(paddle_y):
        """Simulates AI behavior and assigns rewards."""
        future_ball_y = ball.ycor() + (ball.dy * 25)  # Adjusted prediction
        if abs(future_ball_y - paddle_y) < 50:
            return 1  # Positive reward for hitting
        else:
            return -1  # Negative reward for missing
    
    win.listen()
    win.onkeypress(paddle_1_up, "w")
    win.onkeypress(paddle_1_down, "s")

    while True:
        win.update()
        
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)
        ai_move()
        
        if ball.ycor() > 290 or ball.ycor() < -290:
            ball.dy *= -1
        
        if ball.xcor() > 350:
            score_1 += 1
            pen.clear()
            ball.goto(0, 0)
            ball.dx *= -1
            pen.write(f"Player A: {score_1} Player B: {score_2}", align="center", font=("Courier", 24, "normal"))

        elif ball.xcor() < -350:
            score_2 += 1
            pen.clear()
            ball.goto(0, 0)
            ball.dx *= -1
            pen.write(f"Player A: {score_1} Player B: {score_2}", align="center", font=("Courier", 24, "normal"))

        if (ball.xcor() > 340 and paddle_2.ycor() - 50 < ball.ycor() < paddle_2.ycor() + 50):
            ball.setx(340)
            ball.dx *= -1

        if (ball.xcor() < -340 and paddle_1.ycor() - 50 < ball.ycor() < paddle_1.ycor() + 50):
            ball.setx(-340)
            ball.dx *= -1

        time.sleep(0.005)  # Reduced delay for even faster gameplay

Pong()