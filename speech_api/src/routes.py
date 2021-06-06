from app import app
from handlers import index

app.router.add_route('POST', '/', index)
