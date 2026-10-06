import heapq

aristas = [
    ("I", "B", 3), ("I", "F", 7), ("O", "D", 13), ("O", "Q", 7),
    ("B", "D", 5), ("D", "T", 6), ("T", "J", 9), ("D", "E", 2),
    ("T", "E", 2), ("D", "C", 8), ("B", "C", 1), ("B", "S", 4),
    ("A", "N", 5), ("A", "G", 9), ("Q", "N", 4), ("S", "C", 2),
    ("F", "P", 12), ("C", "E", 10), ("C", "P", 21), ("E", "L", 7),
]
grafo = {}
for a, b, w in aristas:
    grafo.setdefault(a, {})[b] = w
    grafo.setdefault(b, {})[a] = w


def dijkstra(grafo, origen):
    dist = {n: float("inf") for n in grafo}
    previo = {}
    dist[origen] = 0
    cola = [(0, origen)]
    cerrados = set()
    while cola:
        d, u = heapq.heappop(cola)
        if u in cerrados:
            continue
        cerrados.add(u)
        for v, peso in grafo[u].items():
            if d + peso < dist[v]:
                dist[v] = d + peso
                previo[v] = u
                heapq.heappush(cola, (dist[v], v))
    return dist, previo


def camino(previo, origen, destino):
    ruta = [destino]
    while ruta[-1] != origen:
        ruta.append(previo[ruta[-1]])
    return ruta[::-1]


farmacias = {
    "B": {"chicles", "antipsicoticos", "vendas"},
    "C": {"supositorios", "aspirinas", "antitusivo"},
    "F": {"chicles", "vendas", "supositorios", "antitusivo"},
    "T": {"antipsicoticos", "aspirinas", "antitusivo"},
}
pedidos = {                      
    "T": {"antitusivo", "chicles"},
    "E": {"supositorios", "vendas"},
    "D": {"antipsicoticos", "aspirinas"},
}
recogida = {}                    
for cliente, productos in pedidos.items():
    validas = [f for f, stock in farmacias.items() if productos <= stock]
    recogida[cliente] = validas[0]
    print(f"Pedido para {cliente}: recoger en {validas[0]}")


pos, total = "S", 0
llevo, entregados = set(), set()
ruta_completa = ["S"]
print()
while len(entregados) < len(pedidos):
    dist, previo = dijkstra(grafo, pos)           
    utiles = []
    for c, f in recogida.items():
        if c in entregados:
            continue
        if c in llevo:
            utiles.append((dist[c], c, "entregar"))   
        else:
            utiles.append((dist[f], f, "recoger"))    
    d, destino, accion = min(utiles)

    tramo = camino(previo, pos, destino)
    ruta_completa += tramo[1:]
    total += d
    print(f"{pos} -> {destino} ({accion}), coste {d}, ruta {'-'.join(tramo)}")

    pos = destino
    for c, f in recogida.items():                
        if f == pos:
            llevo.add(c)
    for c in list(llevo):                         
        if c == pos:
            entregados.add(c)

print("\nRuta completa:", " -> ".join(ruta_completa))
print("Coste total:", total)