from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# from routes.routes_usuarios import router as usuarios_router
from routes.routes_autenticacion import router as autenticacion_router
from routes.routes_metodos_pago import router as metodos_pago_router
# from routes.routes_categorias import router as cateogorias_router
from routes.routes_domicilio import router as domicilios_router
from routes.routes_pedido import router as pedidos_router
from routes.routes_detalle_carrito import router as detalles_carrito_router
# from routes.routes_detalle_pedido import router as detalles_pedido_router
from routes.routes_envio import router as envio_router

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)



# app.include_router(usuarios_router,prefix='/api',tags=["Usuarios"])
app.include_router(autenticacion_router,prefix='/api',tags=["Auth"])
app.include_router(metodos_pago_router,prefix='/api',tags=["Payment Methods"])
# app.include_router(cateogorias_router,prefix='/api',tags=["Categories"])
app.include_router(domicilios_router,prefix='/api',tags=["Addresses"])
app.include_router(pedidos_router, prefix='/api', tags=["Orders"])
app.include_router(detalles_carrito_router, prefix='/api', tags=["Carts"])
# app.include_router(detalles_pedido_router,prefix='/api', tags=["Detalles Pedido"])
app.include_router(envio_router,prefix='/api', tags=["Shippings"])



# url_conection = 'mysql+pymysql://root:123@localhost:3306/pruebas'
# Falta ver bien la logica de pedidos, ya que no se bien aun como debe ser

@app.get("/")
def read_root():
    return {"message": "Hi, FastAPI is working"}