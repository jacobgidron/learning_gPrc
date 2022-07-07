# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import cv2

import grpc
import numpy as np

import jacob_pb2
import jacob_pb2_grpc


class Greeter(jacob_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return jacob_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SayHelloStream(self, request, context):
        for i in range(5):
            yield jacob_pb2.HelloReply(message=f'Hello, {request.name}! call num {i}')

    def camStream(self, request, context):
        print(request.name)
        cap = cv2.VideoCapture(1)
        while True:
            ret, frame = cap.read()
            # frame = bytes(list(frame.flatten()))
            frame = frame.tobytes()
            yield jacob_pb2.Frame(img=frame)

            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    jacob_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()


