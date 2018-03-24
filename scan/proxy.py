from mitmproxy import flow,  controller
from scan.models import  proxy_data

class WSProxy(flow.FlowMaster):
    def __init__(self, opts, server, state, unsave_data):
        super(WSProxy, self).__init__(opts, server, state)
        self.unsave_data = unsave_data
    def run(self):
        try:
            print("start")
            flow.FlowMaster.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    @controller.handler
    def request(self, f):
        wsproxy_request_handle(f)

    @controller.handler
    def response(self, f):
        wsproxy_response_handle(f)
        # parser = ResponseParser(f)
        # insert_result(parser.parser_data())

static_file = ['.js', '.txt', '.mp3', '.css', '.jpg', '.png', '.gif', '.woff', '.ico', '.pdf', '.mp4']

def wsproxy_request_handle(flow):
    """wyproxy send data to server before processing"""
    pass
    # change the request headers['Host']
    # flow.request.headers['X-Online-Host'] = 'wap.gd.10086.cn'

def wsproxy_response_handle(flow):
    path = '/{}'.format('/'.join(flow.request.path_components))
    code = 0
    for i in static_file:  # Exclude static file in capture packet
        if path.find(i) > 0:
            code = 1
            break

    if code == 0:
        # print json.dump(flow.request.headers)
        proxy_data.objects.create(  # save data in database
            host=flow.request.host,
            port=flow.request.port,
            method=flow.request.method,
            url=flow.request.url,
            scheme=flow.request.scheme,
            request_headers=flow.request.headers,
            request_content=flow.request.content,
            path=path,
            status_code=flow.response.status_code,
            response_headers=flow.response.headers,
            response_content=flow.response.content,
            request_cookies=flow.request.cookies,
            http_version=flow.request.http_version
        )