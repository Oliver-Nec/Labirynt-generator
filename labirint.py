import pygame
import random
from collections import deque

pygame.init()
screen = pygame.display.set_mode((1720, 1720))
pygame.display.set_caption("Labirint")
clock = pygame.time.Clock()
running = True
hrac_farba = "#A6A57A"
screen.fill("#27213C")
stena_farba = "#A33B20"
koniec_farba = "#D72638"
player_position = (163,70)
player_width = 50
player_height = 50

end_position = (1570,1480)
hrac_v = (0,0)
hrac_cesta = []
hrac_cesta_set = set(hrac_cesta)

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
    pygame.draw.rect(surface,stena_farba,krab,width=10)

def nove_bludisko():
    cesty_list = nahodna_kostra_grafu(graf_bludiska_list(15,15),(random.randint(0,14),random.randint(0,14)))
    cesty_set = set(cesty_list)
    return cesty_set

def nakresli_bludisko(bludisko_ktore_nakreslit):
    cesty_set = bludisko_ktore_nakreslit
    for i in range(15):
        for j in range(14):
            if (((i,j+1),(i,j)) in cesty_set) or (((i,j),(i,j+1)) in cesty_set):
                pass
            else:
                x_stena = (210+(j*100),20+(i*100))
                y_stena = (210+(j*100),120+(i*100))
                pygame.draw.line(screen,stena_farba,x_stena,y_stena, width = 10)
    for i in range(14):
        for j in range(15):
            if (((i+1,j),(i,j)) in cesty_set) or ((((i,j),(i+1,j)) in cesty_set)):
                pass
            else:
                x_stena = (110+(j*100),120+(i*100))
                y_stena = (210+(j*100),120+(i*100))
                pygame.draw.line(screen,stena_farba,x_stena,y_stena, width = 10)
def da_sa(plapla,smer,bludisko):
    cesty_set = bludisko
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
def bludisko_do_grafu(bludisko,riadky,stlpce):
    graf = {(r,s):[] for r in range(riadky) for s in range(stlpce)}
    for v1,v2 in bludisko:
        graf[v1].append(v2)
        graf[v2].append(v1)
    return graf        

def reset():
    global hrac_v
    global player_position
    global end_position
    global bludisko 
    bludisko = nove_bludisko()
    hrac_cesta.clear()
    hrac_cesta_set.clear()
    player_position = (163,70)
    end_position = (1570,1480)
    hrac_v = (0,0)
    screen.fill("#27213C")
    nakresli_bludisko(bludisko)
    krabica_bez_vnutra(screen,110,20,1510,1510)
    pygame.draw.circle(screen,koniec_farba,end_position,25)

def najdi_cestu(graf,start,ciel):
    fronta = deque([(start, [start])])
    navstivene = {start}

    while fronta:
        sucastny_vrchol, cesta = fronta.popleft()

        if sucastny_vrchol == ciel:
            return cesta  

        for sused in graf[sucastny_vrchol]:
            if sused not in navstivene:
                navstivene.add(sused)
                nova_cesta = cesta + [sused]
                fronta.append((sused, nova_cesta))

    return None

def konvertuj_body(bod):
    y = (bod[0]*100) + 70#y
    x = (bod[1]*100) + 163#x
    return (x,y)


pygame.draw.circle(screen,koniec_farba,end_position,25)
bludisko = nove_bludisko()
nakresli_bludisko(bludisko)
krabica_bez_vnutra(screen,110,20,1510,1510)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_z:
                cesta_do_cielu = najdi_cestu(bludisko_do_grafu(bludisko,15,15),hrac_v,(14,14))
                for i in range(len(cesta_do_cielu)-1):
                    cesta_do_cielu_bod = (konvertuj_body(cesta_do_cielu[i]),konvertuj_body(cesta_do_cielu[i+1]))
                    cesta_do_cielu_bod_segmen = (min(cesta_do_cielu_bod),max(cesta_do_cielu_bod))
                    if cesta_do_cielu_bod_segmen not in hrac_cesta_set:
                        hrac_cesta.append(cesta_do_cielu_bod)
                        hrac_cesta_set.add(cesta_do_cielu_bod_segmen)

            elif event.key == pygame.K_s:
                if da_sa(hrac_v,"d_d",bludisko):
                    new_player_position = (player_position[0],player_position[1]+100)
                    normalizovany_seg = (min(player_position,new_player_position),max(player_position,new_player_position))

                    if normalizovany_seg not in hrac_cesta_set:
                        hrac_cesta.append((player_position,new_player_position))
                        hrac_cesta_set.add(normalizovany_seg)

                    player_position = new_player_position
                    hrac_v = (hrac_v[0]+1,hrac_v[1])
                else:
                    pass
            elif event.key == pygame.K_d:
                if da_sa(hrac_v,"d_p",bludisko):
                    new_player_position = (player_position[0]+100,player_position[1])
                    normalizovany_seg = (min(new_player_position,player_position),max(new_player_position,player_position))

                    if normalizovany_seg not in hrac_cesta_set:
                        hrac_cesta.append((player_position,new_player_position))
                        hrac_cesta_set.add(normalizovany_seg)


                    player_position = new_player_position
                    hrac_v = (hrac_v[0],hrac_v[1]+1)

            elif event.key == pygame.K_a:
                if da_sa(hrac_v,"d_l",bludisko):
                    new_player_position = (player_position[0]-100,player_position[1])
                    normalizovany_seg = (min(new_player_position,player_position),max(new_player_position,player_position))

                    if normalizovany_seg not in hrac_cesta_set:
                        hrac_cesta.append((player_position,new_player_position))
                        hrac_cesta_set.add(normalizovany_seg)
                
                    player_position = new_player_position
                    hrac_v = (hrac_v[0],hrac_v[1]-1)
                

            elif event.key == pygame.K_w:
                if da_sa(hrac_v,"d_h",bludisko):
                    new_player_position = (player_position[0],player_position[1]-100)
                    normalizovany_seg = (min(new_player_position,player_position),max(new_player_position,player_position))
                    if normalizovany_seg not in hrac_cesta_set:
                        hrac_cesta.append((player_position,new_player_position))
                        hrac_cesta_set.add(normalizovany_seg)

                    player_position = new_player_position
                    hrac_v = (hrac_v[0]-1,hrac_v[1])

    screen.fill("#27213C")
    nakresli_bludisko(bludisko)
    krabica_bez_vnutra(screen,110,20,1510,1510)
    pygame.draw.circle(screen,koniec_farba,end_position,25)
    for i in hrac_cesta:
        pygame.draw.line(screen,"#9CF6F6",i[0],i[1],width=10)
    pygame.draw.rect(screen,hrac_farba,[player_position[0]-25,player_position[1]-25,player_width,player_height])

    if hrac_v == (14,14):
        reset()
    # RENDER YOUR GAME HERE

    pygame.display.flip()
    clock.tick(60) 

pygame.quit()
