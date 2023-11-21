# Steven Duplantis
# CS 361
# Microservice for my partner's Exercise App. It returns a picture based on a list containing difficulty and category.

import socket


class MyConnection:

    def __init__(self):
        """
        # Init method for MyConnection object which handles the creation of socket communications
        :param self:
        :return:
        """
        self._host = '127.0.0.1'
        self._port = 4761
        self._my_server = None
        self._client = None
        self._address = None

    def make_connection(self):
        """
        Making a socket connection on local host
        :param self:
        :return: nothing
        """
        self._my_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = 4761
        self._my_server.bind((host, port))
        self._my_server.listen(1)

    def close_connection(self):
        """
        Closing client
        :param self:
        :return: nothing
        """
        self._client.close()

    def get_message(self):
        """
        Gets message from client
        :param self:
        :return: returns message from client
        """
        # Calling make connection to set up sockets
        self.make_connection()
        self._client, self._address = self._my_server.accept()

        # Printing info about connection and message
        print("Connection from: ", self._address)
        new_message = self._client.recv(1024).decode('utf-8')
        print("Received: ", new_message)

        # returning message
        return new_message

    def send_image(self, client_message):
        """
        Sends image to client
        :param client_message: list containing difficulty and category
        :return: nothing
        """

        # Making a connection
        self.make_connection()

        # Taking difficulty & category from list and creating file name
        difficulty, category = eval(client_message)
        file_name_j = 'Images/image' + str(difficulty) + str(category) + '.jpeg'
        file_name_w = 'Images/image' + str(difficulty) + str(category) + '.webp'
        file_name_p = 'Images/image' + str(difficulty) + str(category) + '.png'
        file = None

        # static image file, need to add logic to pick based on category and difficulty
        # since images can be jpeg, png, or webp, we'll use try/except for the different formats
        try:
            file = open(file_name_j, 'rb')
        except FileNotFoundError:
            try:
                file = open(file_name_w, 'rb')
            except FileNotFoundError:
                try:
                    file = open(file_name_p, 'rb')
                except FileNotFoundError:
                    print("No File Found")

        image_data = file.read(2048)

        # While there is binary data to read, keep looping and sending it in chunkies
        while image_data:
            self._client.send(image_data)
            image_data = file.read(2048)

        # Done writing image so close file
        file.close()

        # Closing connection so client knows that the image has been sent in full
        self.close_connection()


# loop to receive instruction from client, and then send image based on message
keep_run = True
new_server = MyConnection()
while keep_run:
    message = new_server.get_message()
    if message == 'close':
        keep_run = False
    else:
        new_server.send_image(message)
