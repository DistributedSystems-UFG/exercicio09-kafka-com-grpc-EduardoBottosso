import grpc

import temperatura_pb2
import temperatura_pb2_grpc


GRPC_SERVER_ADDR = "44.203.64.179"
GRPC_SERVER_PORT = "50051"


def imprimir_alerta(alerta):
    print(f"Sensor: {alerta.sensor_id}")
    print(f"Temperatura: {alerta.temperatura}")
    print(f"Variação: {alerta.variacao}")
    print(f"Unidade: {alerta.unidade}")
    print(f"Classificação: {alerta.classificacao}")
    print(f"Alerta: {alerta.alerta}")
    print(f"Mensagem: {alerta.mensagem}")
    print(f"Timestamp: {alerta.timestamp}")


def main():
    canal = grpc.insecure_channel(f"{GRPC_SERVER_ADDR}:{GRPC_SERVER_PORT}")

    stub = temperatura_pb2_grpc.TemperaturaServiceStub(canal)

    print("Último alerta recebido:")
    resposta_ultimo = stub.ObterUltimoAlerta(
        temperatura_pb2.ConsultaAlertaRequest(sensor_id="")
    )
    imprimir_alerta(resposta_ultimo)

    print("\nLista de alertas recebida:")
    resposta_lista = stub.ListarAlertas(
        temperatura_pb2.ConsultaAlertaRequest(sensor_id="")
    )

    for alerta in resposta_lista.alertas:
        print("-" * 40)
        imprimir_alerta(alerta)


if __name__ == "__main__":
    main()
