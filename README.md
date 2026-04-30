[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/A6uVSc3Y)

KAFKA:
  na maquina chamada 2gb tá rodando kafka:
  cd kafka_2.13-4.2.0/
  
  Enable remote access to the broker: Edit the file config/server.properties (in the kafka directory) in order to change the line starting with advertised_listeners, replacing (only) the first occurrence of localhost with the IP address of the machine where the Broker will run (server01). It is recommended to use a fixed public IP address for this machine. That line should look like this:
  
  advertised.listeners=PLAINTEXT://32.195.37.234:9092,CONTROLLER://localhost:9093
  
  KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
  
  bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties
  
  bin/kafka-server-start.sh config/server.properties
  
  
  Install the Kafka Python client
  sudo apt update
  sudo apt install python3-pip
  sudo apt install python3-venv
  python3 -m venv myvenv
  source myvenv/bin/activate
  pip3 install kafka-python
  
  clientes kafka:
  
  Install the Kafka Python client
  sudo apt update
  sudo apt install python3-pip
  sudo apt install python3-venv
  python3 -m venv myvenv
  source myvenv/bin/activate
  pip3 install kafka-python
  
  Run the Producer on one machine
  python3 producer <topic_name>
  Run the Client on another machine
  python3 consumer <topic_name>



  
