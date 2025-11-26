from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import datetime, timedelta

# ===============================
# Conexión
# ===============================
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "RESTAURANTE_RESERVAS"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
fake = Faker()

with engine.connect() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

    tablas = ["pago", "reservacion", "mesa", "direccion", "telefono", "cliente"]

    # Truncar tablas
    for t in tablas:
        conn.execute(text(f"TRUNCATE TABLE {t}"))

    # ==========================================================
    # 1. Cliente (10)
    # ==========================================================
    for _ in range(10):
        conn.execute(text("""
            INSERT INTO cliente (codigo_cliente, nombre_cliente, correo)
            VALUES (:codigo, :nombre, :correo)
        """), {
            "codigo": fake.bothify("CL-##"),
            "nombre": fake.name(),
            "correo": fake.email()
        })

    # ==========================================================
    # 2. Teléfonos (10)
    # ==========================================================
    for _ in range(10):
        conn.execute(text("""
            INSERT INTO telefono (numero_telefono, id_cliente)
            VALUES (:numero, :cliente)
        """), {
            "numero": fake.phone_number(),
            "cliente": random.randint(1, 10)
        })

    # ==========================================================
    # 3. Direcciones (10)
    # ==========================================================
    for _ in range(10):
        conn.execute(text("""
            INSERT INTO direccion (calle, numero, ciudad, zona, id_cliente)
            VALUES (:calle, :numero, :ciudad, :zona, :cliente)
        """), {
            "calle": fake.street_name(),
            "numero": str(random.randint(1, 999)),
            "ciudad": fake.city(),
            "zona": fake.word(),
            "cliente": random.randint(1, 10)
        })

    # ==========================================================
    # 4. Mesas (10)
    # ==========================================================
    for _ in range(10):
        conn.execute(text("""
            INSERT INTO mesa (numero_mesa, capacidad_mesa)
            VALUES (:numero, :capacidad)
        """), {
            "numero": str(random.randint(1, 50)),
            "capacidad": str(random.choice([2, 4, 6, 8]))
        })

    # ==========================================================
    # 5. Reservaciones (10)
    # ==========================================================
    for _ in range(10):
        fecha = fake.date_between(start_date="today", end_date="+3m")
        hora = datetime.combine(fecha, datetime.min.time()) + timedelta(hours=random.randint(12, 22))
        conn.execute(text("""
            INSERT INTO reservacion (fecha_reservacion, hora, cantidad_personas, estado_reserva, id_cliente, id_mesa)
            VALUES (:fecha, :hora, :cantidad, :estado, :cliente, :mesa)
        """), {
            "fecha": fecha,
            "hora": hora,
            "cantidad": str(random.randint(1, 8)),
            "estado": random.choice(["Pendiente", "Confirmada", "Cancelada"]),
            "cliente": random.randint(1, 10),
            "mesa": random.randint(1, 10)
        })

    # ==========================================================
    # 6. Pagos (10)
    # ==========================================================
    for _ in range(10):
        conn.execute(text("""
            INSERT INTO pago (metodo_pago, total_pagado, id_reservacion)
            VALUES (:metodo, :total, :reservacion)
        """), {
            "metodo": random.choice(["Efectivo", "Tarjeta", "Transferencia"]),
            "total": round(random.uniform(20, 500), 2),
            "reservacion": random.randint(1, 10)
        })

    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    conn.commit()

print("✅ Datos de RESTAURANTE_RESERVAS (10 por tabla) completados.")
