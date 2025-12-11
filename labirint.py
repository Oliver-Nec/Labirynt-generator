import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1720, 1720))
clock = pygame.time.Clock()
running = True

screen.fill("#968684")

player_position = (163,70)
end_position = (1570,1480)
hrac_v = (0,0)


def graf_bludiska_list(riadky,stlpce):
    graf = {}
    smer = [(1,0),(-1,0),(0,1),(0,-1)]
    for r in range(riadky):
        for s in range(stlpce): 
            susedia = []
            for dr,ds in smer:
                nr, ns = r+dr, s+ds
                if 0 <= nr < riadky and 0 <= ns < stlpce:
                    susedia.append((nr,ns))
            graf[(r,s)] = susedia
    return graf

def nahodna_kostra_grafu(graf,start=(0,0)):
    najdene = set()
    listy = []

    def preh_hlbk(vrchol):
        najdene.add(vrchol)
        susedia = list(graf[vrchol])
        random.shuffle(susedia)
        for dalsi_v in susedia:
            if dalsi_v not in najdene:
                listy.append((vrchol,dalsi_v))
                preh_hlbk(dalsi_v)
    
    preh_hlbk(start)


    return listy

def krabica_bez_vnutra(surface,x,y,x2,y2):
    krab = pygame.Rect(x,y,x2,y2)
    pygame.draw.rect(surface,"black",krab,width=10)

def nakresli_bludisko():
    global cesty_list
    global cesty_set

    cesty_list = nahodna_kostra_grafu(graf_bludiska_list(15,15),(random.randint(0,14),random.randint(0,14)))
    cesty_set = set(cesty_list)
    for i in range(15):
        for j in range(14):
            if (((i,j+1),(i,j)) in cesty_set) or (((i,j),(i,j+1)) in cesty_set):
                pass
            else:
                x_stena = (210+(j*100),20+(i*100))
                y_stena = (210+(j*100),120+(i*100))
                pygame.draw.line(screen,"black",x_stena,y_stena, width = 10)
    for i in range(14):
        for j in range(15):
            if (((i+1,j),(i,j)) in cesty_set) or ((((i,j),(i+1,j)) in cesty_set)):
                pass
            else:
                x_stena = (110+(j*100),120+(i*100))
                y_stena = (210+(j*100),120+(i*100))
                pygame.draw.line(screen,"black",x_stena,y_stena, width = 10)

def da_sa(plapla,smer):
    if smer == "d_d":
        if ((plapla,(plapla[0]+1,plapla[1])) in cesty_set) or (((plapla[0]+1,plapla[1]),plapla) in cesty_set):
            return True
        else:
            return False
    elif smer == "d_p":
        if ((plapla,(plapla[0],plapla[1]+1)) in cesty_set) or (((plapla[0],plapla[1]+1),plapla) in cesty_set):
            return True
        else:
            return False 
    elif smer == "d_l":
        if ((plapla,(plapla[0],plapla[1]-1)) in cesty_set) or (((plapla[0],plapla[1]-1),plapla) in cesty_set):
            return True
        else:
            return False
    elif smer == "d_h":
        if ((plapla,(plapla[0]-1,plapla[1])) in cesty_set) or (((plapla[0]-1,plapla[1]),plapla) in cesty_set):
            return True
        else:
            return False
        
def reset():
    global hrac_v
    global player_position
    global end_position
    
    player_position = (163,70)
    end_position = (1570,1480)
    hrac_v = (0,0)
    screen.fill("#968684")
    nakresli_bludisko()
    krabica_bez_vnutra(screen,110,20,1510,1510)
    pygame.draw.rect(screen,"green",hracko)
    pygame.draw.circle(screen,"red",end_position,25)


hracko = pygame.Rect((player_position[0]-25,player_position[1]-25),(50,50))

pygame.draw.rect(screen,"green",hracko)
pygame.draw.circle(screen,"red",end_position,25)
    
nakresli_bludisko()
krabica_bez_vnutra(screen,110,20,1510,1510)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player_position = (163,70)
                end_position = (1570,1480)
                hrac_v = (0,0)
                screen.fill("#968684")
                nakresli_bludisko()
                krabica_bez_vnutra(screen,110,20,1510,1510)
                pygame.draw.rect(screen,"green",hracko)
                pygame.draw.circle(screen,"red",end_position,25)
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_s:
                if da_sa(hrac_v,"d_d"):
                    pygame.draw.line(screen,"green",player_position,(player_position[0],player_position[1]+100), width=10)
                    player_position = (player_position[0],player_position[1]+100)
                    hrac_v = (hrac_v[0]+1,hrac_v[1])
                else:
                    pass
            elif event.key == pygame.K_d:
                if da_sa(hrac_v,"d_p"):
                    pygame.draw.line(screen,"green",player_position,(player_position[0]+100,player_position[1]), width=10)
                    player_position = (player_position[0]+100,player_position[1])
                    hrac_v = (hrac_v[0],hrac_v[1]+1)
            elif event.key == pygame.K_a:
                if da_sa(hrac_v,"d_l"):
                    pygame.draw.line(screen,"green",player_position,(player_position[0]-100,player_position[1]), width=10)
                    player_position = (player_position[0]-100,player_position[1])
                    hrac_v = (hrac_v[0],hrac_v[1]-1)
            elif event.key == pygame.K_w:
                if da_sa(hrac_v,"d_h"):
                    pygame.draw.line(screen,"green",player_position,(player_position[0],player_position[1]-100), width=10)
                    player_position = (player_position[0],player_position[1]-100)
                    hrac_v = (hrac_v[0]-1,hrac_v[1])
    if hrac_v == (14,14):
        print("vyhral si more")
        reset()
    # RENDER YOUR GAME HERE

    pygame.display.flip()
    clock.tick(60) 

pygame.quit()
