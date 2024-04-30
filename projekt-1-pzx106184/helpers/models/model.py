from OpenGL.GL import *


class Model:
	def __init__(self):
		self.vertexCount = 0
		self.vertices = []
		self.normals = []
		self.vertexNormals = []
		self.texCoords = []
		self.colors = []

	def drawWire(self, smooth=False):
		glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
		self.drawSolid(smooth)
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

	def drawSolid(self, smooth=True):
		glEnableVertexAttribArray(0)
		glEnableVertexAttribArray(1)
		glEnableVertexAttribArray(2)
		glEnableVertexAttribArray(3)

		glVertexAttribPointer(0, 4, GL_FLOAT, False, 0, self.vertices)
		if not smooth:
			glVertexAttribPointer(1, 4, GL_FLOAT, False, 0, self.normals)
		else:
			glVertexAttribPointer(1, 4, GL_FLOAT, False, 0, self.vertexNormals)
		glVertexAttribPointer(2, 2, GL_FLOAT, False, 0, self.texCoords)
		glVertexAttribPointer(3, 4, GL_FLOAT, False, 0, self.colors)

		glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		glDisableVertexAttribArray(2)
		glDisableVertexAttribArray(3)
