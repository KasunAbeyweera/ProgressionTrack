import os
from random import randrange
import graphics


progression_data = []


def get_credits(prompt):
    while True:
        try:
            credits = int(input(prompt))
            if credits not in [0, 20, 40, 60, 80, 100, 120]:
                print("Out of range. Please enter credits in the range 0, 20, 40, 60, 80, 100, or 120.")
                continue
            return credits
        except ValueError:
            print("Integer required.")


def predict_outcome(pass_credits, defer_credits, fail_credits):
    total_credits = pass_credits + defer_credits + fail_credits

    if total_credits != 120:
        return "Total incorrect! Please try again."
    if pass_credits == 120:
        return "Progress"
    elif pass_credits == 100:
        return "trailer"
    if fail_credits >= 80:
        return "Exclude"
    else:
        return "retriever"


def draw_histogram(outcomes_count, close_window=True):
    win = graphics.GraphWin("Progression Histogram", 600, 600)
    win.setBackground("white")

    num_outcomes = len(outcomes_count)
    total_count = sum(outcomes_count.values())
    bar_width = max(800 // (2 * num_outcomes), 50)
    x_position = 50

    for outcome, count in outcomes_count.items():
        bar_height = count * 11
        bar_color = graphics.color_rgb(randrange(256), randrange(256), randrange(256))
        bar = graphics.Rectangle(graphics.Point(x_position, 500),
                                 graphics.Point(x_position + bar_width, 500 - bar_height))
        bar.setFill(bar_color)
        bar.draw(win)

        label = graphics.Text(graphics.Point(x_position + bar_width / 2, 520), outcome)
        label.draw(win)

        count_label = graphics.Text(graphics.Point(x_position + bar_width / 2, 500 - bar_height - 20), str(count))
        count_label.draw(win)

        x_position += bar_width + 20
    total_label = graphics.Text(graphics.Point(win.getWidth() / 2, 550), f"Total Outcomes: {total_count}")
    total_label.setSize(14)
    total_label.draw(win)

    if close_window:
        win.getMouse()
        win.close()


def save_to_file(file_path, data):
    with open(file_path, 'w') as file:
        for entry in data:
            file.write(','.join(map(str, entry)) + '\n')


def load_from_file(file_path):
    data = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            # Skip the first line (headers)
            next(file)
            for line in file:
                data.append(list(map(int, line.strip().split(','))))
    return data

def main():
    global progression_data
    outcomes_count = {"Progress": 0, "trailer": 0, "retriever": 0, "Exclude": 0}
    user_input = ""

    file_path = "progression_data.txt"

    progression_data = load_from_file(file_path)

    while user_input.lower() not in ['q']:
        print("Welcome to the progression outcome calculator!\n----------------------------------------------")
        print(
            "Enter your credits at pass, defer, and fail respectively.\n----------------------------------------------")
        try:
            pass_credits = get_credits("Please enter your credits at pass: ")
            defer_credits = get_credits("Please enter your credits at defer: ")
            fail_credits = get_credits("Please enter your credits at fail: ")
            total_credits = pass_credits + defer_credits + fail_credits
            if total_credits != 120:
                print("Total incorrect! Please try again.")
                continue
            if total_credits == 120:
                outcome = predict_outcome(pass_credits, defer_credits, fail_credits)
                print(
                    f"-------------------------------\n Progression outcome = {outcome}\n-------------------------------")
                outcomes_count[outcome] += 1

                progression_data.append([outcome, pass_credits, defer_credits, fail_credits])

            user_input = ""
            while user_input.lower() not in ['y', 'q']:
                user_input = input("Would you like to enter another set of data? Enter 'y' for yes or 'q' to quit: ")
                if user_input.lower() == 'q':
                    break

        except ValueError:
            print("Invalid input. Please enter valid numeric values.")
            continue

    save_to_file(file_path, progression_data)

    print("\nStored Progression Data:")
    for data in progression_data:
        print(f"{data[0]} - {data[1]}, {data[2]}, {data[3]}")

    draw_histogram(outcomes_count, close_window=True)


if __name__ == "__main__":
    main()
