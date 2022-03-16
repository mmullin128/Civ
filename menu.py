import pygame, os, tempfile
#from PIL import Image
pygame.init()
TIMESNEWROMAN = pygame.font.SysFont("arial",20)



def start_menu():
    done = False
    screensize =(300,400)
    fontColor = (100,160,250)
    highlightColor = (100,100,100)
    screen = pygame.display.set_mode(screensize)
    line1 = TIMESNEWROMAN.render('New Game',True,fontColor)
    line1s = TIMESNEWROMAN.render('New Game',True,highlightColor)
    line1size = TIMESNEWROMAN.size('New Game')
        
    line2 = TIMESNEWROMAN.render('Load Game',True,fontColor)
    line2s = TIMESNEWROMAN.render('Load Game',True,highlightColor)
    line2size = TIMESNEWROMAN.size('Load Game')

    line3 = TIMESNEWROMAN.render('Settings',True,fontColor)
    line3s = TIMESNEWROMAN.render('Settings',True,highlightColor)
    line3size = TIMESNEWROMAN.size('Settings')

        
    line4 = TIMESNEWROMAN.render('Quit',True,fontColor)
    line4s = TIMESNEWROMAN.render('Quit',True,highlightColor)
    line4size = TIMESNEWROMAN.size('Quit')

    selector = 1
    while not done:
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_UP] and selector != 1:
                    selector -= 1
                elif pygame.key.get_pressed()[pygame.K_DOWN] and selector != 4:
                    selector += 1
        if selector == 1:
            screen.blit(line1s,(screensize[0]/2-line1size[0]/2,2*screensize[1]/8-line1size[1]/2))
        else:
            screen.blit(line1,(screensize[0]/2-line1size[0]/2,2*screensize[1]/8-line1size[1]/2))
            
        if selector == 2:
            screen.blit(line2s,(screensize[0]/2-line2size[0]/2,3*screensize[1]/8-line2size[1]/2))

        else:
            screen.blit(line2,(screensize[0]/2-line2size[0]/2,3*screensize[1]/8-line2size[1]/2))
            
        if selector == 3:
            screen.blit(line3s,(screensize[0]/2-line3size[0]/2,4*screensize[1]/8-line3size[1]/2))

        else:
            screen.blit(line3,(screensize[0]/2-line3size[0]/2,4*screensize[1]/8-line3size[1]/2))
            
        if selector == 4:
            screen.blit(line4s,(screensize[0]/2-line4size[0]/2,5*screensize[1]/8-line4size[1]/2))

        else:
            screen.blit(line4,(screensize[0]/2-line4size[0]/2,5*screensize[1]/8-line4size[1]/2))

        pygame.display.update()
    pygame.quit()
start_menu()
