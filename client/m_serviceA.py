import socket
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random


def communicate(message):
    # Set up connection
    my_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 4761
    my_server.connect((host, port))
    # sending message
    my_server.send(message.encode())
    # closing connection
    my_server.close()


def rec_image(message):
    # Set up connection
    my_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 4761
    my_server.connect((host, port))
    # sending message
    my_server.send(message.encode())

    # temp static image, add logic based on category and difficulty
    img_file = 'new_pic.jpg'
    file = open(img_file, 'wb')
    image_data = my_server.recv(2048)

    # getting image data
    while image_data:
        file.write(image_data)
        image_data = my_server.recv(2048)

    file.close()

    # closing connection
    my_server.close()

    return img_file


def show_image(image):
    img = mpimg.imread(image)
    imgplot = plt.imshow(img)
    plt.show()


user_input = 0
while user_input != 2:
    user_input = int(input("To send message, press 1. To Quit, press 2. "))
    if user_input == 1:
        difficulty = int(input("Please enter a difficulty (1 - 5): "))
        category = int(input("Please enter a category (1 - 5): "))
        listy = [difficulty, category]
        img_file = rec_image(str(listy))
        show_image(img_file)
    elif user_input == 2:
        communicate('close')
        print("Sent : ", 'close')
