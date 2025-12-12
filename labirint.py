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
player_x_start = 163
player_y_start = 70
bludisko_velkost = 15
player_position = (player_x_start,player_y_start)
player_width = 50
player_height = 50
level = 1
jeden_bliplupak = 1500//bludisko_velkost
font = pygame.font.Font('freesansbold.ttf', 32)
text_level = font.render(f"Level: {level}", True, "black")
text_levelRect = text_level.get_rect()
text_levelRect.center = (100,1680)

text_velkost = font.render(f"Aktualna velkost bludiska: {bludisko_velkost}X{bludisko_velkost}",True,"white")
text_velkostRect = text_velkost.get_rect()
text_velkostRect.center = (500,1680)

end_position = (1570,1480)
hrac_v = (0,0)
hrac_cesta = []
hrac_cesta_set = set(hrac_cesta)

showing_solution = False
solution_start_time = 0

animating_solution = False
solution_path_to_draw = []
solution_animation_index = 0
last_animation_time = 0
animation_speed_ms = 20 

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

def nove_bludisko(velkost):
    cesty_list = nahodna_kostra_grafu(graf_bludiska_list(velkost,velkost),(random.randint(0,velkost-1),random.randint(0,velkost-1)))
    cesty_set = set(cesty_list)
    return cesty_set

def nakresli_bludisko(bludisko_ktore_nakreslit,velkost):
    cesty_set = bludisko_ktore_nakreslit
    jedna_bunka = 1500 // velkost 

    for r in range(velkost):
        for c in range(velkost):
            if c < velkost - 1:
                path_exists = ((r,c),(r,c+1)) in cesty_set or ((r,c+1),(r,c)) in cesty_set
                if not path_exists:
                    x = 110 + (c + 1) * jedna_bunka
                    y_start = 20 + r * jedna_bunka
                    y_end = 20 + (r + 1) * jedna_bunka
                    pygame.draw.line(screen, stena_farba, (x, y_start), (x, y_end), width=10)

            if r < velkost - 1:
                path_exists = ((r,c),(r+1,c)) in cesty_set or ((r+1,c),(r,c)) in cesty_set
                if not path_exists:
                    x_start = 110 + c * jedna_bunka
                    x_end = 110 + (c + 1) * jedna_bunka
                    y = 20 + (r + 1) * jedna_bunka
                    pygame.draw.line(screen, stena_farba, (x_start, y), (x_end, y), width=10)

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

def reset(velkost):
    global hrac_v, player_position, end_position, bludisko, player_y_start, player_x_start, bludisko_velkost, jeden_bliplupak, player_width, player_height
    bludisko_velkost = velkost
    jeden_bliplupak = 1500 // bludisko_velkost
    player_width = jeden_bliplupak * 0.5
    player_height = jeden_bliplupak * 0.5
    player_x_start = 110 + jeden_bliplupak // 2
    player_y_start = 20 + jeden_bliplupak // 2
    bludisko = nove_bludisko(velkost)
    hrac_cesta.clear()
    hrac_cesta_set.clear()
    player_position = (player_x_start,player_y_start)
    end_position = (110 + (velkost - 1) * jeden_bliplupak + jeden_bliplupak // 2, 20 + (velkost - 1) * jeden_bliplupak + jeden_bliplupak // 2)
    hrac_v = (0,0)
    screen.fill("#27213C")
    nakresli_bludisko(bludisko,bludisko_velkost)
    krabica_bez_vnutra(screen,110,20,1510,1510)
    pygame.draw.circle(screen,koniec_farba,end_position,jeden_bliplupak//4)

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

def konvertuj_body(bod,player_x_start,player_y_start,jeden_blipak):
    y = (bod[0]*jeden_blipak) + player_y_start#y
    x = (bod[1]*jeden_blipak) + player_x_start#x
    return (x,y)


pygame.draw.circle(screen,koniec_farba,end_position,jeden_bliplupak//4)
bludisko = nove_bludisko(bludisko_velkost)
nakresli_bludisko(bludisko,bludisko_velkost)
krabica_bez_vnutra(screen,110,20,1510,1510)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset(bludisko_velkost)
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_z:
                if not animating_solution and not showing_solution:
                    #global animating_solution, solution_path_to_draw, solution_animation_index, last_animation_time

                    cesta_do_cielu = najdi_cestu(bludisko_do_grafu(bludisko,bludisko_velkost,bludisko_velkost),hrac_v,(bludisko_velkost-1,bludisko_velkost-1))
                    
                    if cesta_do_cielu:
                        solution_path_to_draw.clear()
                        for i in range(len(cesta_do_cielu)-1):
                            cesta_do_cielu_bod = (konvertuj_body(cesta_do_cielu[i],player_x_start,player_y_start,jeden_bliplupak),konvertuj_body(cesta_do_cielu[i+1],player_x_start,player_y_start,jeden_bliplupak))
                            solution_path_to_draw.append(cesta_do_cielu_bod)
                        
                        hrac_cesta.clear()
                        hrac_cesta_set.clear()
                        solution_animation_index = 0
                        last_animation_time = pygame.time.get_ticks()
                        animating_solution = True
            elif event.key == pygame.K_s:
                if not showing_solution and not animating_solution and da_sa(hrac_v,"d_d",bludisko):
                    new_player_position = (player_position[0],player_position[1]+jeden_bliplupak)
                    normalizovany_seg = (min(player_position,new_player_position),max(player_position,new_player_position))

                    if normalizovany_seg not in hrac_cesta_set:
                        hrac_cesta.append((player_position,new_player_position))
                        hrac_cesta_set.add(normalizovany_seg)

                    player_position = new_player_position
                    hrac_v = (hrac_v[0]+1,hrac_v[1])
                else:
                    pass
            elif event.key == pygame.K_d:
                if not showing_solution and not animating_solution and da_sa(hrac_v,"d_p",bludisko):
                    new_player_position = (player_position[0]+jeden_bliplupak,player_position[1])
                    normalizovany_seg = (min(new_player_position,player_position),max(new_player_position,player_position))

                    if normalizovany_seg not in hrac_cesta_set:
                        hrac_cesta.append((player_position,new_player_position))
                        hrac_cesta_set.add(normalizovany_seg)


                    player_position = new_player_position
                    hrac_v = (hrac_v[0],hrac_v[1]+1)

            elif event.key == pygame.K_a:
                if not showing_solution and not animating_solution and da_sa(hrac_v,"d_l",bludisko):
                    new_player_position = (player_position[0]-jeden_bliplupak,player_position[1])
                    normalizovany_seg = (min(new_player_position,player_position),max(new_player_position,player_position))

                    if normalizovany_seg not in hrac_cesta_set:
                        hrac_cesta.append((player_position,new_player_position))
                        hrac_cesta_set.add(normalizovany_seg)
                
                    player_position = new_player_position
                    hrac_v = (hrac_v[0],hrac_v[1]-1)
                

            elif event.key == pygame.K_w:
                if not showing_solution and not animating_solution and da_sa(hrac_v,"d_h",bludisko):
                    new_player_position = (player_position[0],player_position[1]-jeden_bliplupak)
                    normalizovany_seg = (min(new_player_position,player_position),max(new_player_position,player_position))
                    if normalizovany_seg not in hrac_cesta_set:
                        hrac_cesta.append((player_position,new_player_position))
                        hrac_cesta_set.add(normalizovany_seg)

                    player_position = new_player_position
                    hrac_v = (hrac_v[0]-1,hrac_v[1])

   
    if animating_solution:
        current_time = pygame.time.get_ticks()
        if current_time - last_animation_time > animation_speed_ms:
            if solution_animation_index < len(solution_path_to_draw):
                hrac_cesta.append(solution_path_to_draw[solution_animation_index])
                solution_animation_index += 1
                last_animation_time = current_time
            else:
                animating_solution = False
                showing_solution = True
                solution_start_time = pygame.time.get_ticks()

    if showing_solution:
        if pygame.time.get_ticks() - solution_start_time > 3000: 
            level = 1
            reset(15)
            showing_solution = False

    screen.fill("#27213C")
    nakresli_bludisko(bludisko,bludisko_velkost)
    krabica_bez_vnutra(screen,110,20,1510,1510)
    pygame.draw.circle(screen,koniec_farba,end_position,jeden_bliplupak//4)
    for i in hrac_cesta:
        pygame.draw.line(screen,"#9CF6F6",i[0],i[1],width=10)
    pygame.draw.rect(screen,hrac_farba,[player_position[0]-player_width/2,player_position[1]-player_height/2,player_width,player_height])
    text_level = font.render(f"Level: {level}", True, "white")
    text_velkost = font.render(f"Aktualna velkost bludiska: {bludisko_velkost}X{bludisko_velkost}",True,"white")
    screen.blit(text_level,text_levelRect)
    screen.blit(text_velkost,text_velkostRect)
    

    if hrac_v == (bludisko_velkost-1,bludisko_velkost-1):
        level = level + 1
        reset(15 + (level - 1) * 2)

    pygame.display.flip()
    clock.tick(60) 

pygame.quit()
