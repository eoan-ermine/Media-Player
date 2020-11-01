import pygame

class MidiPlayer:
    class __MidiPlayer:
        def __init__(self, filename):
            self.filename = filename
            
            self.is_loaded = False
            self.is_loop = False
            
        def play(self):
            if not self.is_loaded:
                pygame.mixer.music.load(self.filename)
            pygame.mixer.music.play()

        def stop(self):
            pygame.mixer.music.stop()

        def pause(self):
            pygame.mixer.music.pause()
            
        def unwind(self):
            pygame.mixer.music.unwind()

        def unpause(self):
            pygame.mixer.music.unpause()

        def loop(self, is_loop):
            if (self.is_loop and is_loop) or not (self.is_loop and is_loop):
                return
            position = pygame.mixer.music.get_pos()
            pygame.mixer.music.stop()
            
            pygame.mixer.music.play(-1 if is_loop else 0, position)

        def is_playing(self):
            return pygame.mixer.music.get_busy()

    instance = None
    def __new__(cls, *args, **kwargs):
        if not MidiPlayer.instance:
            frequency = 44100
            bitsize = -16
            channels = 2
            buffer = 1024

            pygame.mixer.init(frequency, bitsize, channels, buffer)

            MidiPlayer.instance = MidiPlayer.__MidiPlayer(*args, **kwargs)
        return MidiPlayer.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)

if __name__ == "__main__":
    import sys
    
    player = MidiPlayer(sys.argv[1])
    player.play()

    while player.is_playing:
        pass
