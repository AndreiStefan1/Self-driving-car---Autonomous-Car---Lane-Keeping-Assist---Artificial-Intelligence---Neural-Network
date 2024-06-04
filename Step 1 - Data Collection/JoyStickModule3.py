import pygame
from time import sleep

pygame.init()

controller = pygame.joystick.Joystick(0)
controller.init()
buttons = {
    'A': 0,
    'axis1': 0., 'axis2': 0., 'axis3': 0., 'axis4': 0.
}

def getJS(name=''):
    global buttons
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                buttons['axis1'] = round(event.value, 2)
            elif event.axis == 1:
                buttons['axis2'] = round(event.value, 2)
            elif event.axis == 2:
                buttons['axis3'] = round(event.value, 2)
            elif event.axis == 3:
                buttons['axis4'] = round(event.value, 2)
        elif event.type == pygame.JOYBUTTONDOWN:
            if controller.get_button(0):  # "A" button is button 0
                buttons['A'] = 1
        elif event.type == pygame.JOYBUTTONUP:
            if not controller.get_button(0):  # "A" button is button 0
                buttons['A'] = 0

    if name == '':
        return buttons
    else:
        return buttons.get(name, 0)

def main():
    joystick_state = getJS()
    print(joystick_state)  # Print the current joystick state
    sleep(1)

if __name__ == '__main__':
    while True:
        main()