import turtle
import tkinter as tk
import tkinter.messagebox

# Create the main window
window = tk.Tk()
window.title("Ping Pong Game by HARPS")

# Create the canvas for the turtle graphics
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()

# Create the turtle screen and set its background color
screen = turtle.TurtleScreen(canvas)
screen.bgcolor("black")

# Create the turtle objects for the paddles, ball, and score
paddle_a = turtle.RawTurtle(screen)
paddle_b = turtle.RawTurtle(screen)
ball = turtle.RawTurtle(screen)
score_a = turtle.RawTurtle(screen)
score_b = turtle.RawTurtle(screen)

# Set the shape, color, and speed of the paddles and ball
paddle_a.shape("square")
paddle_a.color("blue")  # Change the color of paddle A to blue
paddle_a.speed(0)
paddle_b.shape("square")
paddle_b.color("red")  # Change the color of paddle B to red
paddle_b.speed(0)
ball.shape("circle")
ball.color("white")
ball.speed(0)

# Set the size and position of the paddles and ball
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)
ball.penup()
ball.goto(0, 0)

# Set the initial movement of the ball
ball.dx = 5  # Increase the speed of the ball
ball.dy = -5  # Increase the speed of the ball

# Set the initial score of the players
score_a_value = 0
score_b_value = 0

# Set the shape, color, and speed of the score turtles
score_a.shape("square")
score_a.color("white")
score_a.speed(0)
score_b.shape("square")
score_b.color("white")
score_b.speed(0)

# Set the position and alignment of the score turtles
score_a.penup()
score_a.hideturtle()
score_a.goto(-200, 260)
score_a.write("Player A: 0", align="center", font=("Courier", 24, "normal"))
score_b.penup()
score_b.hideturtle()
score_b.goto(200, 260)
score_b.write("Player B: 0", align="center", font=("Courier", 24, "normal"))

# Define the functions to move the paddles up and down
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)

# Bind the keyboard keys to the paddle movement functions
screen.listen()
screen.onkeypress(paddle_a_up, "w")
screen.onkeypress(paddle_a_down, "s")
screen.onkeypress(paddle_b_up, "Up")
screen.onkeypress(paddle_b_down, "Down")

# Define the main game loop
def game_loop():
    global score_a_value, score_b_value
    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Check for the ball hitting the top or bottom border
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
    elif ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    # Check for the ball hitting the right or left border
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        # Update the score of player A
        score_a_value += 1
        score_a.clear()
        score_a.write("Player A: {}".format(score_a_value), align="center", font=("Courier", 24, "normal"))
        # Increase the speed of the ball
        ball.dx += 0.5
        ball.dy += 0.5
    elif ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        # Update the score of player B
        score_b_value += 1
        score_b.clear()
        score_b.write("Player B: {}".format(score_b_value), align="center", font=("Courier", 24, "normal"))
        # Increase the speed of the ball
        ball.dx += 0.5
        ball.dy += 0.5

    # Check for the ball hitting the paddles
    if (ball.xcor() > 340 and ball.xcor() < 350) and (
            ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50):
        ball.setx(340)
        ball.dx *= -1
    elif (ball.xcor() < -340 and ball.xcor() > -350) and (
            ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50):
        ball.setx(-340)
        ball.dx *= -1

    # Check for the game over condition
    if score_a_value == 10 or score_b_value == 10:
        # Stop the ball movement
        ball.dx = 0
        ball.dy = 0
        # Display the winner message
        winner = turtle.RawTurtle(screen)
        winner.shape("square")
        winner.color("white")
        winner.speed(0)
        winner.penup()
        winner.hideturtle()
        if score_a_value == 10:
            winner.write("Player A Wins!", align="center", font=("Courier", 32, "bold"))
        else:
            winner.write("Player B Wins!", align="center", font=("Courier", 32, "bold"))
        # Show the final scores in a new GUI window
        tkinter.messagebox.showinfo("Final Scores",
                                    "Player A: {}\nPlayer B: {}".format(score_a_value, score_b_value))
        # Update the status label
        status.set("Game Over")
    else:
        # Continue the game loop
        screen.ontimer(game_loop, 10)

# Define the function to show the user agreement
def show_user_agreement():
    agreement = """
    User Agreement:
    
    By playing this game, you agree to the following terms:
    
    1. You will abide by the rules and guidelines of the game.
    2. You will not attempt to cheat or use unfair advantage.
    3. You understand that the game may collect anonymous usage data for improvement purposes.
    4. You agree that the developers are not liable for any damages or losses incurred while playing the game.
    
    Enjoy the game responsibly!
    """
    tkinter.messagebox.showinfo("User Agreement", agreement)

# Define the function to start the game
def start_game():
    # Show the user agreement
    show_user_agreement()
    # Start the game loop
    game_loop()
    # Update the status label
    status.set("Game On")

# Define the function to pause the game
def pause_game():
    # Stop the game loop
    ball.dx = 0
    ball.dy = 0
    # Update the status label
    status.set("Game Paused")

# Define the function to restart the game
def restart_game():
    # Reset the position and movement of the paddles and ball
    paddle_a.goto(-350, 0)
    paddle_b.goto(350, 0)
    ball.goto(0, 0)
    ball.dx = 5
    ball.dy = -5
    # Reset the score of the players
    global score_a_value, score_b_value
    score_a_value = 0
    score_b_value = 0
    score_a.clear()
    score_a.write("Player A: 0", align="center", font=("Courier", 24, "normal"))
    score_b.clear()
    score_b.write("Player B: 0", align="center", font=("Courier", 24, "normal"))
    # Restart the game loop
    game_loop()
    # Update the status label
    status.set("Game On")

# Define the function to display the results
def display_results():
    # Show the current scores in a new GUI window
    tkinter.messagebox.showinfo("Current Scores", "Player A: {}\nPlayer B: {}".format(score_a_value, score_b_value))

# Define the function to quit the game
def quit_game():
    window.destroy()

# Create the buttons and label for the options
start_button = tk.Button(window, text="Start Game", command=start_game)
pause_button = tk.Button(window, text="Pause", command=pause_game)
restart_button = tk.Button(window, text="Restart", command=restart_game)
result_button = tk.Button(window, text="Display Results", command=display_results)
quit_button = tk.Button(window, text="Quit", command=quit_game)
instruction_label = tk.Label(window, text="Welcome to the Ping Pong Game by HARPS!\nPlease choose one of the options below to start, pause, restart, display the results, or quit the game.", font=("Courier", 16, "normal"))

# Pack the buttons and label
start_button.pack(pady=10)
pause_button.pack(pady=10)
restart_button.pack(pady=10)
result_button.pack(pady=10)
quit_button.pack(pady=10)
instruction_label.pack(pady=20)

# Create a string variable for the status label
status = tk.StringVar()
status.set("Ready")

# Create a label for the status
status_label = tk.Label(window, textvariable=status, font=("Courier", 16, "normal"))
status_label.pack()

# Mainloop for the window
window.mainloop()
