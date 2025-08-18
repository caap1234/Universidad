from scapy.all import ICMP, IP, sr1

def ping_host(host):
    print(f"\n[+] Enviando ping a {host} ...")
    pkt = IP(dst=host)/ICMP()
    resp = sr1(pkt, timeout=2, verbose=0)
    if resp:
        print(f"[OK] {host} está en línea. Respuesta recibida.")
    else:
        print(f"[X] {host} no responde.")

# Llamada a la función
ping_host("8.8.8.8")
