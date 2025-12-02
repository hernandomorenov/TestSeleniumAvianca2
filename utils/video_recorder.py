import cv2
import pyautogui
import numpy as np
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

class VideoRecorder:
    """Grabador de video para evidencias"""
    
    def __init__(self, fps=15):
        self.fps = fps
        self.recording = False
        self.writer = None
        self.filename = None
        
    def start_recording(self, test_name):
        """Iniciar grabación de pantalla"""
        try:
            # Crear directorio si no existe
            os.makedirs("videos", exist_ok=True)
            
            # Obtener tamaño de pantalla
            screen_size = pyautogui.size()
            
            # Configurar codec
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.filename = f"videos/{test_name}_{timestamp}.mp4"
            
            # Crear VideoWriter
            self.writer = cv2.VideoWriter(
                self.filename, 
                fourcc, 
                self.fps, 
                screen_size
            )
            
            self.recording = True
            logger.info(f"🎥 Grabación iniciada: {self.filename}")
            
        except Exception as e:
            logger.error(f"❌ Error iniciando grabación: {e}")
    
    def capture_frame(self):
        """Capturar un frame"""
        if self.recording and self.writer:
            try:
                # Capturar screenshot
                screenshot = pyautogui.screenshot()
                
                # Convertir a array numpy
                frame = np.array(screenshot)
                
                # Convertir RGB a BGR (OpenCV usa BGR)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Escribir frame
                self.writer.write(frame)
                
            except Exception as e:
                logger.error(f"❌ Error capturando frame: {e}")
    
    def stop_recording(self):
        """Detener grabación"""
        if self.recording and self.writer:
            try:
                self.recording = False
                self.writer.release()
                cv2.destroyAllWindows()
                
                logger.info(f"🎥 Grabación detenida: {self.filename}")
                return self.filename
                
            except Exception as e:
                logger.error(f"❌ Error deteniendo grabación: {e}")
        
        return None