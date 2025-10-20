from fastapi import FastAPI

from routes.routes_usuarios import router as usuarios_router
from routes.routes_autenticacion import router as autenticacion_router
from routes.routes_metodos_pago import router as metodos_pago_router
from routes.routes_categorias import router as cateogorias_router
from routes.routes_domicilio import router as domicilios_router
from routes.routes_pedido import router as pedidos_router
from routes.routes_detalle_carrito import router as detalles_carrito_router
from routes.routes_detalle_pedido import router as detalles_pedido_router
from routes.routes_envio import router as envio_router

app = FastAPI()

app.include_router(usuarios_router,prefix='/api',tags=["Usuarios"])
app.include_router(autenticacion_router,prefix='/api',tags=["Autenticacion"])
app.include_router(metodos_pago_router,prefix='/api',tags=["Metodos de Pago"])
app.include_router(cateogorias_router,prefix='/api',tags=["Categorias"])
app.include_router(domicilios_router,prefix='/api',tags=["Domicilios"])
app.include_router(pedidos_router, prefix='/api', tags=["Pedidos"])
app.include_router(detalles_carrito_router, prefix='/api', tags=["Detalles Carrito"])
app.include_router(detalles_pedido_router,prefix='/api', tags=["Detalles Pedido"])
app.include_router(envio_router,prefix='/api', tags=["Envios"])



# url_conection = 'mysql+pymysql://root:123@localhost:3306/pruebas'

@app.get("/")
def read_root():
    return {"message": "Hi, FastAPI is working"}