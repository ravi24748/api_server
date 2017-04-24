# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.http import HttpResponse

import time
import json

thread_detail = {}
kill_conn = {}


# Create your views here.
class ThreadTimeout(View):

    def get(self,request):
        print ("done")
        conn_id = request.GET.get("connid", 0)
        time_out = request.GET.get("timeout", 1)
        print (conn_id)
        print (time_out)
        t_end = time.time() + int(time_out)

        thread_detail[conn_id] = t_end

        print (thread_detail)

        print ("time.time() is", time.time())
        print ("timeout is", time_out)
        print ("t_end is", t_end)


        killed = False


        while time.time() < t_end:
            if kill_conn.get(conn_id, False) is True:
                killed = True
                kill_conn.pop(conn_id)
                break


        thread_detail.pop(conn_id)

        if killed is True:
            return HttpResponse(json.dumps({"status": "killed"}), status=200)



        return HttpResponse(json.dumps({"status": "ok"}), status=200)


class ThreadStatus(View):

    def get(self, request):

        response = {}

        for key, value in thread_detail.items():
            print (key, value)

            response[key] = value - time.time()

        print ("in serverStatus")
        return HttpResponse(json.dumps(response), status=200)


class ThreadKill(View):

    def put(self, request):

        payload = request.body

        payload = json.loads(payload)

        conn_id = str(payload.get("connid", '0'))

        if thread_detail.get(conn_id) is not None:
            kill_conn[conn_id] = True

            return HttpResponse(json.dumps({"status":"ok"}), status=200)

        return HttpResponse(json.dumps({"status": "invalid", "connection_id": conn_id}), status=200)




