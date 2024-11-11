from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, JSONResponse, HTMLResponse
from sqlmodel import Session
from typing import Annotated
from db import get_db

from db import SessionDep
import crud
from models import User, UserCreate, UserPublic

from port_forwarding_with_httpx import forward_request

# 只禁掉图形化界面, 看看有没有人能 hack 成功
# 毕竟没有权限验证
app = FastAPI(docs_url=False, redoc_url=False)
app = FastAPI() # for test

# TODO: 把 port 分离成子路由

@app.get("/")
def read_root():
    return {"Hello 0lineTekCenter"}


@app.get("/items/{item_id}")
def read_item(item_id: int,request: Request, q: Union[str, None] = None, ):
    print(request.base_url)
    print(request.url)
    print(request.url.path)
    print(request.url.components)
    # print(Request.url_for)
    # return request
    return {"item_id": item_id * 3, "q": q}


# 响应模型对 list 没用, 得手动转换
# @app.get("/port/all", response_class=list[UserPublic])
@app.get("/port/all",)
async def get_all_pair(session: Session = Depends(get_db)) -> list[UserPublic]:
    user_list: list[User] = crud.get_all_users(session=session)
    # 或者也可以这样 UserPublic(**user.dict(exclude_unset=True)) (从官方模板偷的)
    return [UserPublic.from_orm(user) for user in user_list]


@app.get("/port/query/{user_name}")
async def query_port(user_name: str, session: Session = Depends(get_db)) -> int:
    user = crud.get_user_by_full_name(session=session, full_name=user_name)
    if not user:
        raise HTTPException(404, f"User {user_name} not found")
    return user.port

# cannot use session: Annotated[Session, Depends(get_db)]
@app.get("/port/allocate/{user_name}")
async def allocate_port(user_name: str, session: Session = Depends(get_db)) -> int:
    user = crud.get_user_by_full_name(session=session, full_name=user_name)
    if user:
        raise HTTPException(403, "Target name already exists.")
    new_port = rand_port(session=session)
    if not new_port:
        raise HTTPException(500, "Server error. Try again.")
    user = crud.create_user(session=session,
        user_create=UserCreate(
            full_name=user_name,
            port=new_port,
        ))
    return user.port

# range: [8001, 8101), max try: 10 times
# return 0 on failure
def rand_port(session) -> int:
    import random
    begin = 8001
    end = 8101
    max_try = 10

    for i in range(max_try):
        new_port = random.randint(begin, end)
        if not crud.get_user_by_port(session=session, port=new_port):
            return new_port
    
    return 0


# TODO: 迁移成 crud 里的函数
@app.delete("/port/del/{user_name}")
def del_user(user_name: str, session: Session = Depends(get_db)):
    user = crud.get_user_by_full_name(session=session, full_name=user_name)
    if not user:
        raise HTTPException(404)
    
    session.delete(user)
    session.commit()
    return {"message":"ok"}



@app.get("/{user_name}/docs")
async def mock_docs(user_name: str) -> HTMLResponse:
    doc_content: str = f"""<!DOCTYPE html>
<html>
<head>
<link type="text/css" rel="stylesheet" href="docs/swagger-ui.css">
<link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
<title>{user_name}'s backend document</title>
</head>
<body>
<div id="swagger-ui">
</div>
<script src="docs/swagger-ui-bundle.js"></script>
<script>
const ui = SwaggerUIBundle({{
    url: '{user_name}/openapi.json',
"dom_id": "#swagger-ui",
"layout": "BaseLayout",
"deepLinking": true,
"showExtensions": true,
"showCommonExtensions": true,
oauth2RedirectUrl: window.location.origin + '/docs/oauth2-redirect',
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
    ],
}})
</script>
</body>
</html>"""
    return HTMLResponse(content=doc_content)

@app.get("/{user_name}/openapi.json")
async def mock_openapi(user_name: str) -> JSONResponse:
    
    pass

app.mount("/docs", StaticFiles(directory="statics"))



@app.get("/{user_name}/{path:path}")
@app.post("/{user_name}/{path:path}")
@app.delete("/{user_name}/{path:path}")
async def router_forward(user_name: str, path: str, request: Request, session: Session = Depends(get_db)) -> Response:
    return await forward(user_name=user_name,path=path, request=request,session=session)




async def forward(user_name: str, path: str, request: Request, session: Session) -> Response:
    try:
        user_port: int = query_port(user_name=user_name, session=session)
    except Exception:
        # 处理略显粗糙, 先这样吧
        raise HTTPException(404, f"User {user_name} not found. Forwarding denied.")
    host = "https://tutorial.0linetekcenter.tech"
    host = "http://tutorial.localhost"
    #TODO
    response = await forward_request(host, user_port, "/"+user_name, request)
    return response
    
