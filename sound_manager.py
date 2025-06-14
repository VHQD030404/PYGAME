import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        self.muted = False
    def load_music(self, path):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
        except Exception as e:
            print("khong th tat nhac ", e)

    def load_sound(self, name, path):
        """Tải hiệu ứng âm thanh"""
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
            self.sounds[name].set_volume(self.sfx_volume)
        except Exception as e:
            print(f"Không thể tải âm thanh {name}: {e}")

    def play_music(self, loops=-1):
        """Phát nhạc nền (loops=-1 để lặp vô hạn)"""
        if not self.muted:
            pygame.mixer.music.play(loops)

    def play_sound(self, name):
        """Phát hiệu ứng âm thanh"""
        if not self.muted and name in self.sounds:
            self.sounds[name].play()

    def stop_music(self):
        """Dừng nhạc nền"""
        pygame.mixer.music.stop()

    def set_master_volume(self, volume):
        """Đặt volume tổng (ảnh hưởng cả nhạc và hiệu ứng)"""
        self.music_volume = max(0.0, min(1.0, volume))
        self.sfx_volume = max(0.0, min(1.0, volume))

        if not self.muted:
            pygame.mixer.music.set_volume(self.music_volume)
            for sound in self.sounds.values():
                sound.set_volume(self.sfx_volume)

    def get_current_volume(self):
        """Lấy volume hiện tại (trung bình của music và sfx)"""
        return (self.music_volume + self.sfx_volume) / 2

    def toggle_mute(self):
        """Bật/tắt tiếng"""
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.music.set_volume(0)
            for sound in self.sounds.values():
                sound.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.music_volume)
            for sound in self.sounds.values():
                sound.set_volume(self.sfx_volume)
