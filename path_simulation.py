import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

color_set = ['g', 'r', 'c', 'm', 'y', 'k', 'w']

def dog_path(x, A, k):

    return ( (-1/2) * (A**(1/k)) * (k/(-1+k)) * ((A-x)**((-1+k)/k))
         + (1/2) * (A**(-1/k)) * (k/(1+k)) * ((A-x)**((1+k)/k)) + (k/((k**2)-1))*A ) 

def dog_and_man_paths(k, A, v, duration):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xticks(np.arange(0, max(A)+3, 0.5))
    ax.set_yticks(np.arange(0, max(A)+1, 0.25))

    # store the path of each man and dog
    man_lines = [] 
    dog_lines = []

    def init():
        for line in man_lines + dog_lines:
            line.set_data([], [])
        return man_lines + dog_lines
    
    def animate(frame):
        dog_x = np.zeros(frame)
        dog_y = np.zeros(frame)
        for i, dis in enumerate(A):
            man_x = dis
            man_y = np.arange(0, k / ((k**2) - 1) * dis, v)[:frame]
            man_y = np.clip(man_y, 0, k / ((k**2) - 1) * dis)

            dog_x = np.arange(0, dis + 1, v * (k**2 - 1) / k)[:frame]
            dog_x = np.clip(dog_x, 0, dis)

            dog_y = dog_path(dog_x, dis, k)[:frame]

            man_lines[i].set_data(man_x, man_y)
            dog_lines[i].set_data(dog_x, dog_y)

        return man_lines + dog_lines

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Man and Dog Paths')

    for i, dis in enumerate(A):
        dis = float(dis)
        man_line, = ax.plot([], [], label=f"Man's Path (A = {dis})", color = 'b', linewidth = 2)
        dog_line, = ax.plot([], [], label=f"Dog's Path (A = {dis})", color = color_set[i], linewidth = 2)

        man_lines.append(man_line)
        dog_lines.append(dog_line)

    plt.legend()
    plt.grid()

    anim = FuncAnimation(fig, animate, init_func = init, frames = duration, repeat = True, interval=0.1)
    plt.show()

if __name__ == "__main__":
    while True:
        mode = input("Enter the mode (1 for sample parameter, 2 for user defined parameters): ")
        if mode == "1":
            # sample parameter
            k = 2
            A = [1, 3, 5]
            break
        elif mode == "2":
            # user defined parameter
            k = float(input("Enter the value of k: "))
            A = input("Enter the value of A (use space to separate them): ").split()
            A = list(map(float, A))
            break
        else:
            print("Invalid mode! Please try again.")
    v = 0.005  # Constant speed of the man
    duration = 10000  # Number of frames for animation

    dog_and_man_paths(k, A, v, duration)
