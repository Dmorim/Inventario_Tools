import base64
from PIL import Image
from io import BytesIO
class TelaInicial:
    gear_base64_image = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAe9JREFUOE+lk89r02AYx7/P223dOtAmVTaGouJBvHn2B548C968DOevNGIvZWOplzWXbo7R4Rg0we0gQ4Vdx27iQeb/IMOLKMUemrTDrdU17yNJ15JSsx3MKbz5Pp/3+32eJ4T/fCiqfm6OB4bHnUkwRLx58DabPd/4l7YHwMy0vL6nZB+fdhbt2mVPyq9+EQncMjR1p7hWV+vfT9VMk2QH1gX4xQuWs8xMD0jAYA/XSEBrC/kNGNtMWBUsthqV5NMOpAsorO6lIA53iUg9oS2/RMu7Mps5Ww7chcXzlnMfjHedM2bsByLCaMhy2tBVuydCfpOHhp3aVZacBiF9ZPtV86c67b/Hx9wiETJHRRtSUvFPovbFnLrUDBwUrOojYloL3/y7oiRNk1r+mW3zYNVz3R4nRLeNtPIpAMyXqg8BWg8DUjFF0TQ6jAIwcPOFrn4OAP7MRyfqFzxPTocirKiiHcFpuUUIPG8PBAbF8L5RVn74k+hp4oLlZph55bgmguWd3LMzH/r24OXr6jmvRbsEjBw3RgbKKaFc7MTrWySA7hH4iQTdJUDv2iZ8kwxLEHKGrpb6HATxmGlpo5KYmRzfL5ScGwTsBGMcjKX89c7b5URemzgIO4z8mXxx3Bu6DhqQOT35MSpWJOCEde5+/gti0dERS+LuZQAAAABJRU5ErkJggg=="
    gear_decode_image = base64.b64decode(gear_base64_image)
    gear_image_tela_inicial = Image.open(BytesIO(gear_decode_image))
    
    help_base64_image = ",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"
    help_decode_image = base64.b64decode(help_base64_image)
    help_image_tela_inicial = Image.open(BytesIO(help_decode_image))

class Tutorial:
    tut_img_01 = "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"
    tut_img_01_decode = base64.b64decode(tut_img_01)
    tut_img_01_tutorial = Image.open(BytesIO(tut_img_01_decode))