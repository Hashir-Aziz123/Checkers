import consts

def getPosFromMouseCords(mouse_x, mouse_y):
    row = (mouse_y - consts.CENTER_OFFSET / 4) // consts.SQUARE_SIZE
    col = (mouse_x - consts.CENTER_OFFSET) // consts.SQUARE_SIZE
    return int(row), int(col)  
