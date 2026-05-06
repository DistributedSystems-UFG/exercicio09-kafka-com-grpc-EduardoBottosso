import grpc

import temperatura_pb2
import temperatura_pb2_grpc


GRPC_SERVER_ADDR = "44.203.64.179"
GRPC_SERVER_PORT = "50051"


def main():
    canal = grpc.insecure_channel(f"{GRPC_SERVER_ADDR}:{GRPC_SERVER_PORT}")

    stub = temperatura_pb2_grpc.TemperaturaServiceStub(canal)

    resposta = stub.ObterUltimoAlerta(
        temperatura_pb2.ConsultaAlertaRequest(sensor_id="")
    )

    print("Último alerta recebido:")
    print(f"Sensor: {resposta.sensor_id}")
    print(f"Temperatura: {resposta.temperatura}")
    print(f"Variação: {resposta.variacao}")
    print(f"Unidade: {resposta.unidade}")
    print(f"Classificação: {resposta.classificacao}")
    print(f"Alerta: {resposta.alerta}")
    print(f"Mensagem: {resposta.mensagem}")
    print(f"Timestamp: {resposta.timestamp}")


if __name__ == "__main__":
    main()
