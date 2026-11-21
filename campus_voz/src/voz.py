
import asyncio
import speech_recognition as sr
import flet_audio_recorder as far


FRECUENCIA = 44100
CANALES = 1


class ReconocimientoVoz:

    def __init__(self):
        self.audio = bytearray()
        self.recorder = far.AudioRecorder(
            on_stream=self.recibir_audio
        )

    def recibir_audio(self, evento):
        self.audio.extend(evento.chunk)

    def registrar_servicio(self, page):
        page.services.append(self.recorder)

    async def comenzar_grabacion(self):
        self.audio.clear()

        permiso = await self.recorder.has_permission()

        if not permiso:
            raise RuntimeError(
                "No se concedió permiso para utilizar el micrófono."
            )

        configuracion = far.AudioRecorderConfiguration(
            encoder=far.AudioEncoder.PCM16BITS,
            sample_rate=FRECUENCIA,
            channels=CANALES,
        )

        iniciado = await self.recorder.start_recording(
            configuration=configuracion
        )

        if not iniciado:
            raise RuntimeError(
                "No se pudo iniciar la grabación."
            )

        return True

    async def finalizar_grabacion(self):
        await self.recorder.stop_recording()

        if not self.audio:
            raise RuntimeError(
                "No se detectó audio. Intenta hablar nuevamente."
            )

        audio_capturado = bytes(self.audio)

        resultado = await asyncio.to_thread(
            self.convertir_a_texto,
            audio_capturado
        )

        return resultado

    @staticmethod
    def convertir_a_texto(audio_bytes):

        reconocedor = sr.Recognizer()

        audio = sr.AudioData(
            audio_bytes,
            FRECUENCIA,
            2
        )

        try:
            texto = reconocedor.recognize_google(
                audio,
                language="es-CL"
            )

            return texto

        except sr.UnknownValueError:
            raise RuntimeError(
                "No pude entender lo que dijiste. Intenta nuevamente."
            )

        except sr.RequestError:
            raise RuntimeError(
                "No se pudo conectar con el servicio de reconocimiento "
                "de voz. Comprueba tu conexión a Internet."
            )
