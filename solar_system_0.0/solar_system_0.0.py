#start 4/12/2022
#end 4/14/2022
import math
import pygame
import time

pygame.init()

G = 6.6740831 * 10**-11

class planet:

    def __init__(self, mass, diameter, T, distance_to_sun, distance_to_earth):
        self.m = mass
        self.r = diameter/2
        self.T = T
        self.dis_sun = distance_to_sun
        self.dis_earth = distance_to_earth
    
def centrifugal_acceleration(w, r):
    return w**2 * r

def gravity_acceleration(m, r):
    return G * m/r**2

sun = planet(1.9891 * 10**30, 1.392 * 10**9, 0, 0, 0) # kg, m
mercury = planet(3.3022 * 10**23, 2439.7 * 2 * 10**3  , 87.9691 * 24 * 3600, 57.915 * 10**9, 0) # kg, m
venus = planet(4.8685 * 10**24, 6051.8 * 2 * 10**3  , 224.698 * 24 * 3600, 108.2 * 10**9, 0) # kg, m
earth = planet(5.97237 * 10**24 , 12756.28 * 10**3, 365.25696 * 24 * 3600, 149.6 * 10**9, 0) # kg, m
moon = planet(73.4767 * 10**21, 1738.139 * 2 * 10**3  , 27.32161150 * 24 * 3600, 0, 384 * 10**6) # kg, m
mar = planet(6.4171*10**23, 3396.2 * 2 * 10**3  , 686.980 * 24 * 3600, 228 * 10**9,0) # kg, m
jupiter = planet(1.8986 * 10**27, 71492 * 2 * 10**3  , 4332.59 * 24 * 3600, 778 * 10**9,0) # kg, m

WIDTH, HEIGHT = 1500, 700

GREEN = (0,200,0)
BLUE = (0,0,200)
BLACK = (0,0,0)
RED = (200,0,0)
ORG = (255,69,0)
SILVER = (137,137,137)
WHITE = (255,255,255)
JUP = (253, 206,156)
MOON =(153, 153, 102)

sun_x = 750
sun_y = 300

t = 0 #time

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
running = True

earth_image = pygame.image.load('earth.jpg')
earth_image = pygame.transform.scale(earth_image,(earth.r/10**5.3,earth.r/10**5.3))

moon_image = pygame.image.load('moon1.jpg')
moon_image = pygame.transform.scale(moon_image,(moon.r/10**5.3,moon.r/10**5.3))

sun_image = pygame.image.load('images.png')
sun_image = pygame.transform.scale(sun_image,(sun.r/10**7.2,sun.r/10**7.2))

while running:
    clock.tick(60)
    screen.fill(BLACK)

    #draw sun
    # pygame.draw.circle(screen, RED, (sun_x,sun_y),sun.r/10**7.5)
    screen.blit(sun_image, (sun_x, sun_y))

    #draw mercury
    mercury_x = sun_x - mercury.dis_sun/10**9 * math.sin(2*math.pi/mercury.T * t)
    mercury_y = sun_y - mercury.dis_sun/10**9 * math.cos(2*math.pi/mercury.T * t)
    pygame.draw.circle(screen, SILVER, (mercury_x, mercury_y), mercury.r/10**6)
    # pygame.draw.line(screen, SILVER, (sun_x, sun_y) ,(mercury_x, mercury_y))

    #draw venus
    venus_x = sun_x - venus.dis_sun/10**9 * math.sin(2*math.pi/venus.T * t)
    venus_y = sun_y - venus.dis_sun/10**9 * math.cos(2*math.pi/venus.T * t)
    pygame.draw.circle(screen, WHITE, (venus_x, venus_y), venus.r/10**6)
    # pygame.draw.line(screen, WHITE, (sun_x, sun_y) ,(venus_x, venus_y))

    #draw earth
    earth_x = sun_x - earth.dis_sun/10**9 * math.sin(2*math.pi/earth.T * t)
    earth_y = sun_y - earth.dis_sun/10**9 * math.cos(2*math.pi/earth.T * t)
    screen.blit(earth_image, (earth_x-15, earth_y-15))
    # pygame.draw.circle(screen, BLUE, (earth_x, earth_y), earth.r/10**5.7)
    # pygame.draw.line(screen, BLUE, (sun_x, sun_y) ,(earth_x, earth_y))

    #draw moon
    moon_x = earth_x - moon.dis_earth/10**7.1 * math.sin(2*math.pi/moon.T * t)
    moon_y = earth_y - moon.dis_earth/10**7.1 * math.cos(2*math.pi/moon.T * t)
    screen.blit(moon_image, (moon_x, moon_y))
    # pygame.draw.circle(screen, MOON, (moon_x, moon_y), moon.r/10**5.7)
    # pygame.draw.line(screen, MOON, (earth_x, earth_y) ,(moon_x, moon_y))

    #draw mar
    mar_x = sun_x - mar.dis_sun/10**9 * math.sin(2*math.pi/mar.T * t)
    mar_y = sun_y - mar.dis_sun/10**9 * math.cos(2*math.pi/mar.T * t)
    pygame.draw.circle(screen, ORG, (mar_x, mar_y), mar.r/10**6)
    # pygame.draw.line(screen, ORG, (sun_x, sun_y) ,(mar_x, mar_y))

    #draw jupiter
    jupiter_x = sun_x - jupiter.dis_sun/10**9/3 * math.sin(2*math.pi/jupiter.T * t)
    jupiter_y = sun_y - jupiter.dis_sun/10**9/3 * math.cos(2*math.pi/jupiter.T * t)
    pygame.draw.circle(screen, JUP, (jupiter_x, jupiter_y), jupiter.r/10**6.8)
    # pygame.draw.line(screen, JUP, (sun_x, sun_y) ,(jupiter_x, jupiter_y))




    t+= 3600*10
    
    if earth.dis_sun <=0:
        earth.dis_sun = 0
    else:
        mercury.dis_sun = mercury.dis_sun - gravity_acceleration(sun.m, mercury.dis_sun) + centrifugal_acceleration(2*math.pi/mercury.T, mercury.dis_sun)
        # print(mercury.dis_sun)

        venus.dis_sun = venus.dis_sun - gravity_acceleration(sun.m, venus.dis_sun) + centrifugal_acceleration(2*math.pi/venus.T, venus.dis_sun)
        # print(venus.dis_sun)

        earth.dis_sun = earth.dis_sun - gravity_acceleration(sun.m, earth.dis_sun) + centrifugal_acceleration(2*math.pi/earth.T, earth.dis_sun)
        # print(earth.dis_sun)

        moon.dis_earth = moon.dis_earth - gravity_acceleration(earth.m, moon.dis_earth) + centrifugal_acceleration(2*math.pi/moon.T, moon.dis_earth)
        print(moon.dis_earth)
    
        mar.dis_sun = mar.dis_sun - gravity_acceleration(sun.m, mar.dis_sun) + centrifugal_acceleration(2*math.pi/mar.T, mar.dis_sun)
        # print(mar.dis_sun)

        jupiter.dis_sun = jupiter.dis_sun - gravity_acceleration(sun.m, jupiter.dis_sun) + centrifugal_acceleration(2*math.pi/jupiter.T, jupiter.dis_sun)
        # print(jupiter.dis_sun)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()



