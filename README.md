# Taichi 图形课 S1

## Lecture01

### N body problem

- Change symplectic euler to midpoint method
- Add a mouse event (click to mimic a black hole)

![N body](./images/N-body.png)

### Julia set

- Change the recurrence relation to $z = z^4 + c$ (shape)
- Change the color of this animation to RGB, using a simple linear blended colormap

![Julia set](./images/Julia_set.png)

## Lecture02

### Galaxy

- Change the mass of the stars on the fly (Controlled by GUI widgets -- a scrollbar)
- Add another class of SuperStars with:
    - different visualization (OrangeRed)
    - different initialization (distributed on the diagonal)
    - orders of magnitudes heavier

![Galaxy](./gifs/galaxy3-1.gif)