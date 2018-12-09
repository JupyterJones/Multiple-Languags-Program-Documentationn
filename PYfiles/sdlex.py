# https://stackoverflow.com/questions/22374120/create-pixel-square-and-present-later
import sys
import sdl2
import sdl2.ext
import numpy

SIZE_X = 400
SIZE_Y = 300

# RGB values
RED = 0xFF0000
GREEN = 0x00FF00

def pixelate():
    choices = [RED, GREEN]
    pixelarray = numpy.random.choice(choices,(SIZE_X, SIZE_Y))
    buf = pixelarray.tostring()
    # Create a software surface from the array. The depth and pitch are really
    # important here, since we use a continuous byte buffer access.
    image = sdl2.SDL_CreateRGBSurfaceFrom(buf,
                                          SIZE_X, SIZE_Y,
                                          32,   # Bit depth, we use 32-bit RGB
                                          SIZE_X, # pitch (byte size of a single scanline) - for 32 bit it is SIZE_X
                                          0xFF0000,
                                          0x00FF00,
                                          0x0000FF,
                                          0x0)
    # required to avoid loosing buf. SDL_CreateRGBSurfaceFrom() will
    # reference the byte buffer, not copy it
    image._buffer = buf
    return image

def main():
    sdl2.ext.init()

    window = sdl2.ext.Window("Pixel example", size=(800, 600))
    imgoffset = sdl2.SDL_Rect(200, 150, 0, 0)
    window.show()

    # Software rendering, we also could use hardware rending and use streaming
    # textures, but the example would become more complicated then.
    windowsurface = window.get_surface()

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                image = pixelate()
                sdl2.SDL_BlitSurface(image, None, windowsurface, imgoffset)
        window.refresh()
        sdl2.SDL_Delay(10)
    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())