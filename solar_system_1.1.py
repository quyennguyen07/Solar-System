import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1200, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")

WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
GREEN = (0, 153, 0)

SUN = (255, 222, 59)
MER = (227, 227, 227)
VENUS = (150, 131, 150)
EARTH = (100, 149, 237)
MARS = (156, 46, 53)
JUPITER = (167, 156, 134)
SATURN = (197, 171, 110)
URANUS = (213, 251, 252)
NEPTUNE = (62, 84, 232)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149597870700 #m
    G = 6.6740831 * 10**-11
    SCALE = 200 / AU # 1AU == 200 pixel
    TIMESTEP =  3600*10   # 1 day

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.name = name
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, screen):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
            update_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                update_points.append((x, y))
            pygame.draw.lines(screen, self.color, False, update_points)

        pygame.draw.circle(screen, self.color, (x, y), self.radius)

        # if not self.sun:
        #     distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
        #     screen.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

    def attraction(self, other):
        other_x , other_y = other.x, other.y
        distance_x = self.x - other_x
        distance_y = self.y - other_y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance
        
        alpha = math.atan2(distance_y, distance_x)
        gravity_acceleration = self.G * self.mass / distance**2
        acceleration_x = math.cos(alpha) * gravity_acceleration
        acceleration_y = math.sin(alpha) * gravity_acceleration
        #######################################
        # print("--------------")
        # print(self.name + " tác dụng lên "+ other.name)
        # print(distance_x, distance_y)
        # print(alpha * 180/math.pi)
        # print(acceleration_x, acceleration_y)
        ########################################
        return acceleration_x, acceleration_y

    def update_position(self, planets):
        '''
        Trong lập trình, ta thường sử dụng phương pháp tính toán dựa trên khoảng thời gian cố định
        (fixed timestep), trong đó một khoảng thời gian cố định được sử dụng để tính toán vị trí và 
        vận tốc mới của các vật thể trong một khung cảnh vật lý. Phương pháp này sẽ đảm bảo rằng các 
        tính toán sẽ được thực hiện với cùng một khoảng thời gian, giúp đảm bảo tính ổn định và chính 
        xác của mô phỏng.
        Vì vậy, trong trường hợp này, ta nên sử dụng công thức s = vt để tính toán khoảng cách di chuyển 
        của các vật thể trong một khoảng thời gian cố định, và không nên sử dụng công thức 
        s = vt + 1/2 *a *t**2 vì nó là công thức tính khoảng cách di chuyển với thời gian biến đổi.
        '''
        total_acc_x = total_acc_y = 0
        for planet in planets:
            if planet == self:
                continue
        
            acc_x, acc_y = planet.attraction(self)
            total_acc_x += acc_x
            total_acc_y += acc_y
        
        self.x_vel = self.x_vel + total_acc_x*self.TIMESTEP
        self.y_vel = self.y_vel + total_acc_y*self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        
        self.orbit.append((self.x, self.y))
        

def main():

    Sun = Planet(0, 0, 30, SUN, 1.9891 * 10**30, "Sun")
    Sun.sun = True

    Mercury = Planet(0.387 * Planet.AU, 0, 4.878, MER, 3.3011 * 10**23, "Mercury")
    Mercury.y_vel = -47.36 * 10**3

    Venus = Planet(0.723 * Planet.AU, 0, 12.104, VENUS, 4.8675 * 10**24, "Venus")
    Venus.y_vel = -35.02 * 10**3

    Earth = Planet(1 * Planet.AU , 0, 12.756, EARTH, 5.97237 * 10**24, "Earth")
    Earth.y_vel = -29.783 * 10**3

    Mars = Planet(1.524 * Planet.AU, 0, 6.787, MARS, 6.4171 * 10**23, "Mars")
    Mars.y_vel = -24.007 * 10**3

    Jupiter = Planet(5.204267 * Planet.AU, 0, 20, JUPITER, 1.8982 * 10**27, "Jupiter")
    Jupiter.y_vel = -13.07 * 10**3

    Saturn = Planet(9 * Planet.AU, 0, 18, SATURN, 5.6834 * 10**26, "Saturn")
    Saturn.y_vel = -9.68 * 10**3

    Uranus = Planet(20 * Planet.AU, 0, 15, URANUS, 8.6810 * 10**25, "Uranus")
    Uranus.y_vel = -6.80 * 10**3

    Neptune = Planet(30.1 * Planet.AU, 0, 15, NEPTUNE, 1.0243 * 10**26, "Neptune")
    Neptune.y_vel = -5.43 * 10**3


    planets = [Sun, Mercury, Venus, Earth, Mars]

    run = True
    clock = pygame.time.Clock()

    while run:
        # Chạy 60 vòng lặp trong 1s
        clock.tick(60)
        
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(screen)

        pygame.display.flip()

    pygame.quit()

main()