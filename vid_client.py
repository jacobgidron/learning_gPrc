import asyncio
import logging

import cv2

import grpc
import numpy as np

import jacob_pb2
import jacob_pb2_grpc


async def run() -> None:
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = jacob_pb2_grpc.GreeterStub(channel)
        response = await stub.SayHello(jacob_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)

        print("now for steam ")
        async for response in stub.camStream(jacob_pb2.HelloRequestStream(name='you')):
            frame = np.frombuffer(response.img, dtype=np.uint8)
            # frame = np.array(response.img, dtype=np.uint8)
            frame = frame.reshape((480, 640, 3))
            # print(frame.shape)
            # print(frame)
            cv2.imshow("frame", frame)
            cv2.waitKey(1)
            # print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
