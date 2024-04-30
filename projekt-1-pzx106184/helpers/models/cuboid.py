from typing import List
from glm import vec3, vec4, normalize, cross
from . import Model


class Cuboid(Model):
    """
    Klasa do tworzenia prostopadłościanów, każda ściana składa się z 2 trójkątów, dziedziczy po Model,
    konstruktor build_cuboid do tworzenia o podanych wymiarach.
    """
    def __init__(self, width: float = 2.0, height: float = 5.0, depth: float = 2.0):
        super().__init__()
        self.build_cuboid(width, height, depth)

    def compute_face_normal(self, face: List[vec4]) -> vec4:
        # Metoda obliczająca wektor dla danej ściany
        a = vec3(face[1] - face[0])
        b = vec3(face[2] - face[0])
        return normalize(vec4(cross(a, b), 0.0))

    def add_face(self, v1: vec4, v2: vec4, v3: vec4, v4: vec4, color: vec4):
        # Dodanie ściany prostopadłościanu
        self.addVec4(self.vertices, v1)
        self.addVec4(self.vertices, v2)
        self.addVec4(self.vertices, v3)
        self.addVec4(self.vertices, v3)
        self.addVec4(self.vertices, v4)
        self.addVec4(self.vertices, v1)

        normal = self.compute_face_normal([v1, v2, v3])
        for x in range(6):
            self.addVec4(self.normals, normal)
            self.addVec4(self.colors, color)

    def addVec4(self, target: List[float], value: vec4):
        # Pomocnicza funkcja do dodawania obiektu typu vec4 do listy
        target.extend(value)

    def build_cuboid(self, width: float, height: float, depth: float):
        w = width / 2.0
        h = height / 2.0
        d = depth / 2.0

        p0 = vec4(-w, -h, -d, 1.0)
        p1 = vec4(w, -h, -d, 1.0)
        p2 = vec4(w, h, -d, 1.0)
        p3 = vec4(-w, h, -d, 1.0)
        p4 = vec4(-w, -h, d, 1.0)
        p5 = vec4(w, -h, d, 1.0)
        p6 = vec4(w, h, d, 1.0)
        p7 = vec4(-w, h, d, 1.0)

        gray = vec4(0.75, 0.75, 0.75, 1.0)

        self.add_face(p0, p1, p2, p3, gray)  # front
        self.add_face(p4, p5, p6, p7, gray)  # back
        self.add_face(p1, p5, p6, p2, gray)  # right
        self.add_face(p0, p4, p7, p3, gray)  # left
        self.add_face(p3, p2, p6, p7, gray)  # top
        self.add_face(p0, p1, p5, p4, gray)  # bottom

        self.vertexCount = len(self.vertices) // 4
