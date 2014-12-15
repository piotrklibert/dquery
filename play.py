import json
import requests

data = list(json.load(open("sample3.json")))

# try:
#     from betterprint import pprint
# except ImportError:
#     from pprint import pprint


# hostname = "http://localhost"


# from tenclouds.functional import dict_without

# def walk_trace(reqs):
#     for r in reqs:
#         meta = dict_without(r, "req", "resp")
#         yield (r["req"], r["resp"], meta)

# def make_request(req, meta):
#     return requests.request(
#         meta["method"],
#         hostname + meta["uri"],
#         params=json.loads(meta["args"]),
#         headers=req["header"],
#         data=req.get("body",""),
#         verify=False,
#         allow_redirects=False
#     )


# class ReqData(object):


# l =[]
# for req, resp, meta in walk_trace(data):
#     # pprint((dict_without(req, "body"), dict_without(resp, "body"), meta))

#     result = make_request(req, meta)

#     print meta["method"], result, result.cookies

#     import difflib
#     d = difflib.Differ()
#     l.append(list(d.compare(result.content.strip().splitlines(),
#                     resp["body"].strip().splitlines())))

#     print resp["body"].strip() == result.content.strip()
#     print result.content.strip()
