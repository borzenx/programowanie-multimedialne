from OpenGL.GL import *


class ShaderProgram:
	def __init__(self, vert: str, geom: str = "", frag: str = ""):
		self.shaderProgram = 0
		self.construct(vert, geom, frag)

	def construct(self, vert: str, geom: str, frag: str):
		vertexShader = self.loadShader(GL_VERTEX_SHADER, vert)
		geometryShader = 0x7FFFFFFF
		if geom != "":
			geometryShader = self.loadShader(GL_GEOMETRY_SHADER, geom)
		fragmentShader = self.loadShader(GL_FRAGMENT_SHADER, frag)

		self.shaderProgram = glCreateProgram()
		glAttachShader(self.shaderProgram, vertexShader)
		if geometryShader != 0x7FFFFFFF:
			glAttachShader(self.shaderProgram, geometryShader)
		glAttachShader(self.shaderProgram, fragmentShader)
		glLinkProgram(self.shaderProgram)

		log = glGetProgramInfoLog(self.shaderProgram)
		if len(log) > 1:
			print(log)

		glDetachShader(self.shaderProgram, fragmentShader)
		if geometryShader != 0x7FFFFFFF:
			glDetachShader(self.shaderProgram, geometryShader)
		glDetachShader(self.shaderProgram, vertexShader)

		glDeleteShader(fragmentShader)
		if geometryShader != 0x7FFFFFFF:
			glDeleteShader(geometryShader)
		glDeleteShader(vertexShader)

	def __del__(self):
		glDeleteProgram(self.shaderProgram)

	def use(self):
		glUseProgram(self.shaderProgram)

	def u(self, name: str) -> int:
		return glGetUniformLocation(self.shaderProgram, name)

	def a(self, name: str) -> int:
		return glGetAttribLocation(self.shaderProgram, name)

	@staticmethod
	def loadShader(shaderType: int, source_path: str) -> int:
		# Remove non-ASCII characters
		with open(source_path) as source_file:
			source = "".join(
				char for char in source_file.read() if 0 <= ord(char) <= 127
			)
		shader = glCreateShader(shaderType)
		glShaderSource(shader, source)
		glCompileShader(shader)

		log = glGetShaderInfoLog(shader)
		if len(log) > 1:
			print(log)

		return shader


class DemoShaders:
	spConstant = None
	spColored = None
	spLambert = None
	spTextured = None
	spLambertTextured = None

	@staticmethod
	def initShaders(dir: str):
		DemoShaders.spTextured = ShaderProgram(
			vert=dir + "v_textured.glsl", frag=dir + "f_textured.glsl"
		)

		DemoShaders.spConstant = ShaderProgram(
			vert=dir + "v_constant.glsl", frag=dir + "f_constant.glsl"
		)
		DemoShaders.spColored = ShaderProgram(
			vert=dir + "v_colored.glsl", frag=dir + "f_colored.glsl"
		)
		DemoShaders.spLambert = ShaderProgram(
			vert=dir + "v_lambert.glsl", frag=dir + "f_lambert.glsl"
		)
		DemoShaders.spLambertTextured = ShaderProgram(
			vert=dir + "v_lamberttextured.glsl", frag=dir + "f_lamberttextured.glsl"
		)
