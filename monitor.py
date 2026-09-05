import pyshark
import time
import json

last_packet_time = 0

def packets_handler(packet):
    global last_packet_time, packets
    
    current_time = time.time()
    packets = []
    
    # Обрабатываем только если прошла секунда
    if current_time - last_packet_time >= 1.0:
        last_packet_time = current_time
        
        # ВСЁ, ЧТО ЗДЕСЬ - БУДЕТ РАЗ В СЕКУНДУ
        if hasattr(packet, 'ip'):
            src = packet.ip.src
            dst = packet.ip.dst
            
            if hasattr(packet, 'tcp'):
                proto = 'TCP'
                sport = packet.tcp.srcport
                dport = packet.tcp.dstport
            elif hasattr(packet, 'udp'):
                proto = 'UDP'
                sport = packet.udp.srcport
                dport = packet.udp.dstport
            else:
                proto = 'OTHER'
                sport = '-'
                dport = '-'


            packet_data = {
                'time': current_time,
                'src': src,
                'dst': dst,
                'sport': sport,
                'dport': dport,
                'proto': proto,
                'size': int(packet.length)
            }

            packets.append(packet_data)

            if len(packets) > 500:
                packets = packets[-500:]
            
            print(f"[{len(packets)}] from {src} -to-> {dst} | {packet.length} byte")
    # Если условие не выполнено - сюда не заходим, пакет игнорируется

sel_if = input("Type interface name (Wi-Fi/Ethernet): ")

capture = pyshark.LiveCapture(interface=sel_if)
with open("traffic_data.json", "w") as f:
        json.dump(packets, f)

for packet in capture.sniff_continuously():
            packets_handler(packet)

