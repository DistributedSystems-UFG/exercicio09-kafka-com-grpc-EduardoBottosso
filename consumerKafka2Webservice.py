from concurrent import futures
from kafka import KafkaConsumer
from const import *
import grpc
import json
import threading

import temperatura_pb2
import temperatura_pb2_grpc

TOPICO_ENTRADA = TOPICO_ALERTAS

alertas = []
ultimo_alerta_por_sensor = {}


def consumir_alertas_kafka():
    consumer = KafkaConsumer(
        TOPICO_ENTRADA,
        bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT],
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="grupo-grpc-alertas-temperatura"
    )

    print(f"Consumindo eventos do tópico Kafka: {TOPICO_ENTRADA}")

    for mensagem in consumer:
        evento = mensagem.value

        alertas.append(evento)
        ultimo_alerta_por_sensor[evento["sensor_id"]] = evento

        print(f"Alerta recebido do Kafka: {evento}")


class TemperaturaService(temperatura_pb2_grpc.TemperaturaServiceServicer):

    def ObterUltimoAlerta(self, request, context):
        sensor_id = request.sensor_id

        if sensor_id:
            evento = ultimo_alerta_por_sensor.get(sensor_id)
        else:
            evento = alertas[-1] if alertas else None

        if evento is None:
            return temperatura_pb2.AlertaResponse(
                sensor_id="",
                temperatura=0.0,
                variacao=0.0,
                unidade="",
                classificacao="sem_dados",
                alerta=False,
                mensagem="Nenhum alerta encontrado",
                timestamp=""
            )

        return temperatura_pb2.AlertaResponse(
            sensor_id=evento["sensor_id"],
            temperatura=evento["temperatura"],
            variacao=evento["variacao"],
            unidade=evento["unidade"],
            classificacao=evento["classificacao"],
            alerta=evento["alerta"],
            mensagem=evento["mensagem"],
            timestamp=evento["timestamp"]
        )

    def ListarAlertas(self, request, context):
        sensor_id = request.sensor_id

        if sensor_id:
            eventos_filtrados = [
                evento for evento in alertas
                if evento["sensor_id"] == sensor_id
            ]
        else:
            eventos_filtrados = alertas

        respostas = []

        for evento in eventos_filtrados:
            respostas.append(
                temperatura_pb2.AlertaResponse(
                    sensor_id=evento["sensor_id"],
                    temperatura=evento["temperatura"],
                    variacao=evento["variacao"],
                    unidade=evento["unidade"],
                    classificacao=evento["classificacao"],
                    alerta=evento["alerta"],
                    mensagem=evento["mensagem"],
                    timestamp=evento["timestamp"]
                )
            )

        return temperatura_pb2.ListaAlertasResponse(alertas=respostas)


def iniciar_servidor_grpc():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    temperatura_pb2_grpc.add_TemperaturaServiceServicer_to_server(
        TemperaturaService(),
        servidor
    )

    servidor.add_insecure_port("[::]:50051")
    servidor.start()

    print("Servidor gRPC rodando na porta 50051")

    servidor.wait_for_termination()


if __name__ == "__main__":
    thread_kafka = threading.Thread(target=consumir_alertas_kafka)
    thread_kafka.daemon = True
    thread_kafka.start()

    iniciar_servidor_grpc()
