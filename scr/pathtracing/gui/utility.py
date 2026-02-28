import os
import pygame

class FileUtility:
    absolutePath: str = os.getcwd()
    
    @staticmethod
    def import_image(*path, alpha = True):
        fullPath = os.path.join(FileUtility.absolutePath, *path)
        return pygame.image.load(fullPath).convert_alpha() if alpha else pygame.image.load(fullPath).convert()

    @staticmethod
    def import_folder(*path) -> list[pygame.Surface]:
        frames: list[pygame.Surface] = []
        for folderPath, _, imageNames in os.walk(os.path.join(FileUtility.absolutePath, *path)):
            imageNames = [name for name in imageNames if name.endswith( ".png")]
            for imageName in [name.split('.')[0] for name in imageNames]:
                path = os.path.join(folderPath, imageName)
                frames.append(pygame.image.load(path).convert_alpha())
        return frames
    
    @staticmethod
    def import_folder_dict(*path) -> dict[str, pygame.Surface]:
        print(FileUtility.absolutePath)
        frames: dict[str, pygame.Surface] = {}
        for folderPath, _, imageNames in os.walk(os.path.join(FileUtility.absolutePath, *path)):
            imageNames = [name for name in imageNames if name.endswith( ".png")]
            for image_name in [name.split('.')[0] for name in imageNames]:
                path = os.path.join(folderPath, image_name + '.png')
                frames[image_name] = pygame.image.load(path).convert_alpha()
        return frames

    @staticmethod
    def import_subfolders(*path) -> dict[str, list[pygame.Surface]]:
        frames: dict[str, list[pygame.Surface]] = {}
        for _, subfolders, _ in os.walk(os.path.join(FileUtility.absolutePath, *path)):
            for subfolder in subfolders:
                frames[subfolder] = FileUtility.import_folder(*path, subfolder)
        return frames