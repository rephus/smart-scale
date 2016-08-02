import wiiboard
import pygame
import time
from balance import Balance
from bluetooth import BluetoothError
import subprocess

MAX_STABLE_WEIGHTS = 20

def log(msg, level= "INFO"):
    now = time.strftime('%m-%d %H:%M')
    print("{now} - {level}: {msg}".format(**locals()))

def blink (board, times=10):
    for x in range(0,times):

        board.setLight(False)
        time.sleep(0.05)
        board.setLight(True)
        time.sleep(0.05)

def round2(number):
    return float("{0:.2f}".format(number))

def all_same(items):
    tolerance = 0.2
    return all(x + tolerance> items[0] and x - tolerance < items[0] for x in items)

def add_list(items, item):
    if len(items) > 9:
        items = items[1:]

    items.append(item)
    return items

def disconnect_devices():
    #https://github.com/InitialState/beerfridge/blob/master/wiiboard_test.py#L282
    try:
       log("Disconnecting devices")
       # Disconnect already-connected devices.
       # This is basically Linux black magic just to get the thing to work.
       subprocess.check_output(["bluez-test-input", "disconnect", address], stderr=subprocess.STDOUT)
       subprocess.check_output(["bluez-test-input", "disconnect", address], stderr=subprocess.STDOUT)
    except:
       pass

def main():
    try:
        lastWeights = []

        balance = Balance()
        board = wiiboard.Wiiboard()

        pygame.init()

        #address = board.discover()
        address = "78:A2:A0:22:28:E8"

        disconnect_devices()

        log("Connecting to wiiboard address {}".format(address))
        board.connect(address) #The wii board must be in sync mode at this time
        log("Board connected")

        time.sleep(0.1)
        board.setLight(True)


        while True:

            if int(time.time() % 60) == 0:
                blink(board, times=1)
                time.sleep(1)

            time.sleep(0.05)
            events = pygame.event.get()
            #if len(events) > 10:
            #    print("Too many elements on queue {}".format(len(events)))

            for event in events:
                if event.type == wiiboard.WIIBOARD_MASS:
                    weight = event.mass.totalWeight
                    if (weight > 40):
                        #print "Total weight: {}. Top left: {} ".format(weight, event.mass.topLeft)


                        weight = round2(weight) # Weight becomes a string
                        lastWeights = add_list(lastWeights,weight)

                        if len(lastWeights) == MAX_STABLE_WEIGHTS and all_same(lastWeights):

                            if weight > 60:
                                user = "javi"
                            else:
                                user = "mar"

                            log("Saving weight {weight} for user {user}".format(**locals()))
                            balance.save(weight, user)

                            lastWeights = []

                            blink(board)
                            board.setLight(False)

                            for x in range(0,25): # Sleeps for 2.5 seconds while emptying queue
                                pygame.event.clear()
                                time.sleep(0.1)

                            board.setLight(True)
                    elif lastWeights:
                        log("Removing cached weights {}".format(lastWeights))
                        lastWeights = []

                #else:
                #    print ("Got different event type {}".format(event.type))
    except KeyboardInterrupt as e:
        log("Interrupt, exiting...")

        if board:
            log("Disconnecting board")
            board.disconnect()

    except BluetoothError as e:
        log("Got bluetooth error {}".format(e), level = "ERROR")

        if board:
            log("Disconnecting board")
            board.disconnect()
            main() #Retrying
    except Exception as e:
        log("Got unexpected error {}".format(e), level = "ERROR")
        if board:
            log("Disconnecting board")
            board.disconnect()
            main() #Retrying


#Run the script if executed
if __name__ == "__main__":
	main()
