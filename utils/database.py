import sqlite3
import os
from datetime import datetime
from utils.config import Config
from utils.logger import logger

class TestDatabase:
    """Base de datos para almacenar resultados de pruebas"""
    
    def __init__(self, db_name="test_results.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.initialize_database()
    
    def initialize_database(self):
        """Inicializar base de datos y crear tablas"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            
            # Tabla de resultados de tests
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_case TEXT NOT NULL,
                    browser TEXT NOT NULL,
                    status TEXT NOT NULL,
                    duration REAL,
                    start_time DATETIME,
                    end_time DATETIME,
                    error_message TEXT,
                    screenshot_path TEXT,
                    video_path TEXT
                )
            ''')
            
            # Tabla de steps
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_steps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_result_id INTEGER,
                    step_name TEXT,
                    step_status TEXT,
                    step_duration REAL,
                    timestamp DATETIME,
                    FOREIGN KEY (test_result_id) REFERENCES test_results (id)
                )
            ''')
            
            self.connection.commit()
            logger.info(f"✅ Base de datos inicializada: {self.db_name}")
            
        except sqlite3.Error as e:
            logger.error(f"❌ Error inicializando base de datos: {e}")
    
    def insert_test_result(self, test_case, browser, status, duration=None, 
                          error_message=None, screenshot_path=None, video_path=None):
        """Insertar resultado de test"""
        try:
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            end_time = start_time if not duration else None
            
            self.cursor.execute('''
                INSERT INTO test_results 
                (test_case, browser, status, duration, start_time, end_time, 
                 error_message, screenshot_path, video_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (test_case, browser, status, duration, start_time, end_time,
                  error_message, screenshot_path, video_path))
            
            test_id = self.cursor.lastrowid
            self.connection.commit()
            
            logger.info(f"✅ Resultado guardado: {test_case} - {status}")
            return test_id
            
        except sqlite3.Error as e:
            logger.error(f"❌ Error guardando resultado: {e}")
            return None
    
    def insert_test_step(self, test_result_id, step_name, step_status, step_duration=None):
        """Insertar step de test"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.cursor.execute('''
                INSERT INTO test_steps 
                (test_result_id, step_name, step_status, step_duration, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (test_result_id, step_name, step_status, step_duration, timestamp))
            
            self.connection.commit()
            return True
            
        except sqlite3.Error as e:
            logger.error(f"❌ Error guardando step: {e}")
            return False
    
    def get_test_results(self, test_case=None, browser=None, status=None):
        """Obtener resultados de tests"""
        try:
            query = "SELECT * FROM test_results WHERE 1=1"
            params = []
            
            if test_case:
                query += " AND test_case = ?"
                params.append(test_case)
            
            if browser:
                query += " AND browser = ?"
                params.append(browser)
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            query += " ORDER BY start_time DESC"
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
            
        except sqlite3.Error as e:
            logger.error(f"❌ Error obteniendo resultados: {e}")
            return []
    
    def close(self):
        """Cerrar conexión a la base de datos"""
        if self.connection:
            self.connection.close()
            logger.info("✅ Conexión a base de datos cerrada")