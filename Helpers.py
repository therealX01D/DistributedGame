import pygame
def scaleImage(img , factorWidth , factorHeight):
    size = (round(img.get_width()*factorWidth),round(img.get_height()*factorHeight))
    return pygame.transform.scale(img,size)

def blit_rotate_center(win,image,top_left,angle):
    rot_img = pygame.transform.rotate(image,angle)
    #https://drive.google.com/file/d/1rjERvIuPIhj6xOtnZtrPs25GXa2LJhnC/view?usp=sharing
    new_rect = rot_img.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rot_img, new_rect.topleft)
def blit_text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200))
    win.blit(render, (win.get_width()/2 - render.get_width() /
                      2, win.get_height()/2 - render.get_height()/2))