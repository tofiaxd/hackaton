
from conexiones import supabase

try:
    respuesta = (
        supabase.table("usuarios")
        .select("*")
        .limit(5)
        .execute()
    )

    print("¡Conexión exitosa con Supabase!")
    print("Datos:", respuesta.data)

except Exception as error:
    print("Error al consultar Supabase:")
    print(error)
