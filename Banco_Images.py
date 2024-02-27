import base64
from PIL import Image
from io import BytesIO
class TelaInicial:
    gear_base64_image = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAe9JREFUOE+lk89r02AYx7/P223dOtAmVTaGouJBvHn2B548C968DOevNGIvZWOplzWXbo7R4Rg0we0gQ4Vdx27iQeb/IMOLKMUemrTDrdU17yNJ15JSsx3MKbz5Pp/3+32eJ4T/fCiqfm6OB4bHnUkwRLx58DabPd/4l7YHwMy0vL6nZB+fdhbt2mVPyq9+EQncMjR1p7hWV+vfT9VMk2QH1gX4xQuWs8xMD0jAYA/XSEBrC/kNGNtMWBUsthqV5NMOpAsorO6lIA53iUg9oS2/RMu7Mps5Ww7chcXzlnMfjHedM2bsByLCaMhy2tBVuydCfpOHhp3aVZacBiF9ZPtV86c67b/Hx9wiETJHRRtSUvFPovbFnLrUDBwUrOojYloL3/y7oiRNk1r+mW3zYNVz3R4nRLeNtPIpAMyXqg8BWg8DUjFF0TQ6jAIwcPOFrn4OAP7MRyfqFzxPTocirKiiHcFpuUUIPG8PBAbF8L5RVn74k+hp4oLlZph55bgmguWd3LMzH/r24OXr6jmvRbsEjBw3RgbKKaFc7MTrWySA7hH4iQTdJUDv2iZ8kwxLEHKGrpb6HATxmGlpo5KYmRzfL5ScGwTsBGMcjKX89c7b5URemzgIO4z8mXxx3Bu6DhqQOT35MSpWJOCEde5+/gti0dERS+LuZQAAAABJRU5ErkJggg=="
    gear_decode_image = base64.b64decode(gear_base64_image)
    gear_image_tela_inicial = Image.open(BytesIO(gear_decode_image))