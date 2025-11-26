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
DB_NAME = "INVENTARIO_DB"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
fake = Faker()

with engine.connect() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

    tablas = ["compra_item", "item", "telefono_empresa", "direccion_empresa", "proveedor_empresa", "categoria_item"]

    # Truncar tablas
    for t in tablas:
        conn.execute(text(f"TRUNCATE TABLE {t}"))

    # ==========================================================
    # 1. Categoria_item (10)
    # ==========================================================
    for _ in range(10):
        conn.execute(text("""
            INSERT INTO categoria_item (precio_unitario, cantidad_stock, estado_item)
            VALUES (:precio, :cantidad, :estado)
        """), {
            "precio": str(round(random.uniform(5, 500), 2)),
            "cantidad": str(random.randint(1, 100)),
            "estado": random.choice(["Disponible", "Agotado", "Reservado"])
        })

    # ==========================================================
    # 2. Proveedor_empresa (10)
    # ==========================================================
    for _ in range(10):
        conn.execute(text("""
            INSERT INTO proveedor_empresa (nombre_empresa)
            VALUES (:nombre)
        """), {
            "nombre": fake.company()
        })

    # ==========================================================
    # 3. Item (10)
    # ==========================================================
    for _ in range(10):
        conn.execute(text("""
            INSERT INTO item (codigo_item, nombre_item, id_categoria_item)
            VALUES (:codigo, :nombre, :categoria)
        """), {
            "codigo": fake.bothify("IT-###"),
            "nombre": fake.word().capitalize(),
            "categoria": random.randint(1, 10)
        })

    # ==========================================================
    # 4. Compra_item (10)
    # ==========================================================
    for _ in range(10):
        fecha = fake.date_between(start_date="-1y", end_date="today")
        conn.execute(text("""
            INSERT INTO compra_item (fecha_compra, precio_compra, id_proveedor_empresa, id_item)
            VALUES (:fecha, :precio, :proveedor, :item)
        """), {
            "fecha": fecha,
            "precio": round(random.uniform(10, 1000), 2),
            "proveedor": random.randint(1, 10),
            "item": random.randint(1, 10)
        })

    # ==========================================================
    # 5. Direccion_empresa (10)
    # ==========================================================
    for _ in range(10):
        conn.execute(text("""
            INSERT INTO direccion_empresa (ciudad, numero, calle, zona, id_proveedor_empresa)
            VALUES (:ciudad, :numero, :calle, :zona, :proveedor)
        """), {
            "ciudad": fake.city(),
            "numero": str(random.randint(1, 999)),
            "calle": fake.street_name(),
            "zona": fake.word(),
            "proveedor": random.randint(1, 10)
        })

    # ==========================================================
    # 6. Telefono_empresa (10)
    # ==========================================================
    for _ in range(10):
        conn.execute(text("""
            INSERT INTO telefono_empresa (numero_telefono, id_proveedor_empresa)
            VALUES (:telefono, :proveedor)
        """), {
            "telefono": fake.phone_number(),
            "proveedor": random.randint(1, 10)
        })

    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    conn.commit()

print("✅ Datos de INVENTARIO_DB (10 por tabla) completados.")
