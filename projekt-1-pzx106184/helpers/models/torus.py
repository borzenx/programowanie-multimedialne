from typing import List
from glm import vec3, vec4, radians, cross, normalize, cos, sin

from . import Model


class Torus(Model):
	def __init__(
		self,
		R: float = 0.75,
		r: float = 0.25,
		mainDivs: float = 20,
		tubeDivs: float = 20,
	):
		super().__init__()
		self.buildTorus(R, r, mainDivs, tubeDivs)

	def generateTorusPoint(self, R: float, r: float, alpha: float, beta: float) -> vec4:
		alpha = radians(alpha)
		beta = radians(beta)
		return vec4(
			(R + r * cos(alpha)) * cos(beta),
			(R + r * cos(alpha)) * sin(beta),
			r * sin(alpha),
			1.0,
		)

	def computeVertexNormal(self, alpha: float, beta: float) -> vec4:
		alpha = radians(alpha)
		beta = radians(beta)
		return vec4(
			cos(alpha) * cos(beta),
			cos(alpha) * sin(beta),
			sin(alpha),
			0.0,
		)

	def computeFaceNormal(self, face: List[vec4]) -> vec4:
		a = vec3(face[1] - face[0])
		b = vec3(face[2] - face[0])
		return normalize(vec4(cross(b, a), 0.0))

	def generateTorusFace(
		self,
		vertices: List[vec4],
		vertexNormals: List[vec4],
		faceNormal: vec4,
		R: float,
		r: float,
		alpha: float,
		beta: float,
		step_alpha: float,
		step_beta: float,
	):
		vertices[0] = self.generateTorusPoint(R, r, alpha, beta)
		vertices[1] = self.generateTorusPoint(R, r, alpha + step_alpha, beta)
		vertices[2] = self.generateTorusPoint(
			R, r, alpha + step_alpha, beta + step_beta
		)
		vertices[3] = self.generateTorusPoint(R, r, alpha, beta + step_beta)

		faceNormal = self.computeFaceNormal(vertices)

		vertexNormals[0] = self.computeVertexNormal(alpha, beta)
		vertexNormals[1] = self.computeVertexNormal(alpha + step_alpha, beta)
		vertexNormals[2] = self.computeVertexNormal(
			alpha + step_alpha, beta + step_beta
		)
		vertexNormals[3] = self.computeVertexNormal(alpha, beta + step_beta)

		return vertices, vertexNormals, faceNormal

	def addVec4(self, target: List[float], value: vec4):
		target.extend(value)

	def buildTorus(self, R: float, r: float, mainDivs: float, tubeDivs: float):
		face = [vec4(), vec4(), vec4(), vec4()]
		faceVertexNormals = [vec4(), vec4(), vec4(), vec4()]
		normal = vec4()

		internalVertices = []
		internalFaceNormals = []
		internalVertexNormals = []
		internalColors = []

		mult_alpha = 360.0 / tubeDivs
		mult_beta = 360.0 / mainDivs

		green = vec4(0, 1, 0, 1)

		for alpha in range(round(tubeDivs)):
			for beta in range(round(mainDivs)):
				face, faceVertexNormals, normal = self.generateTorusFace(
					face,
					faceVertexNormals,
					normal,
					R,
					r,
					alpha * mult_alpha,
					beta * mult_beta,
					mult_alpha,
					mult_beta,
				)

				self.addVec4(internalVertices, face[0])
				self.addVec4(internalVertices, face[1])
				self.addVec4(internalVertices, face[2])

				self.addVec4(internalVertices, face[0])
				self.addVec4(internalVertices, face[2])
				self.addVec4(internalVertices, face[3])

				self.addVec4(internalVertexNormals, faceVertexNormals[0])
				self.addVec4(internalVertexNormals, faceVertexNormals[1])
				self.addVec4(internalVertexNormals, faceVertexNormals[2])

				self.addVec4(internalVertexNormals, faceVertexNormals[0])
				self.addVec4(internalVertexNormals, faceVertexNormals[2])
				self.addVec4(internalVertexNormals, faceVertexNormals[3])

				for _ in range(6):
					self.addVec4(internalFaceNormals, normal)
					self.addVec4(internalColors, green)

		self.vertices = internalVertices
		self.normals = internalFaceNormals
		self.vertexNormals = internalVertexNormals
		self.colors = internalColors
		self.vertexCount = len(internalVertices) // 4

		self.texCoords = [0.0] * (self.vertexCount * 2)
		for i in range(self.vertexCount):
			self.texCoords[2 * i] = self.vertexNormals[4 * i]
			self.texCoords[2 * i + 1] = self.vertexNormals[4 * i + 1]
