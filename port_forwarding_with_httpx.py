from fastapi import Request
from fastapi.responses import Response
import httpx


async def forward_request(target_host: str, target_port: int, prefix: str, request: Request) -> Response:
    # 必须以 prefix 开头
    assert request.url.path.startswith(prefix)

    # 这里设置你想要转发到的地址和端口
    forward_url = target_host + ":" + str(target_port)
    print("no bug before forwarding")

    # "/abc/de".lstrip("/abc") 返回了 "de" 而不是 "/de"
    # integral_url = forward_url + request.url.path.lstrip(prefix)
    integral_url = forward_url + request.url.path[len(prefix)::]
    # print(request.url.path)
    # print(prefix)
    print(integral_url)

    # 提取请求头部，转换为字典
    headers = {key: value for key, value in request.headers.items()}
    print(headers)
    # 提取cookies，转换为字典
    cookies = request.cookies
    print(cookies)
    
    # 提取查询参数，转换为字典
    query_params = request.query_params._dict
    print(query_params)



    # 转发请求
    # gpt 的回答是错误的, 一些细节还是得自己查文档
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=integral_url,
            headers=headers,
            cookies=cookies,
            params=query_params,
            data=await request.body(),
        )
    
    print("no bug before returning")
    # 返回转发后的响应
    return Response(
        status_code=response.status_code,
        headers={key: value for key, value in response.headers.items()},
        content=response.content,
    )
