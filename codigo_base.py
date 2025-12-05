from tello_sim_EDRA import Simulator

# ----------------------------
# CONFIGURAÇÃO INICIAL DO SIMULADOR
# ----------------------------
# Cria o simulador 
drone = Simulator()

# ----------------------------
# DECOLAGEM
# ----------------------------
drone.takeoff()

# Movimentos iniciais de exemplo
drone.forward(50)
drone.right(30)
drone.right(50)

# ----------------------------
# DICAS DE FUNÇÕES E ATRIBUTOS
# ----------------------------
# Movimentos(cm):
#   drone.forward(dist), drone.back(dist), drone.left(dist), drone.right(dist)
#   drone.cw(deg), drone.ccw(deg)
#
# Status do drone:
#   drone.cur_loc               -> posição atual do drone (x, y)
#   drone.visited_treasures     -> índices dos tesouros já coletados
#   drone.treasures             -> número total de tesouros
#
#
# Coleta automática de tesouros:
#   O simulador verifica automaticamente após cada movimento se algum tesouro
#   foi coletado, mas você pode checar manualmente usando:
#   drone.collect_treasure()
#

# ----------------------------
# TODO: Planejar a rota estratégica
# para coletar todos os tesouros uma vez cada
# ----------------------------
# Dicas de abordagem:
#   - Use loops para percorrer tesouros restantes
#   - Calcule distância entre drone.cur_loc e tesouros
#   - Planeje a sequência para minimizar movimentos
#   - Utilize funções de rotação e deslocamento para se mover de forma eficiente

# Exemplo de verificação de status
print(f"Drone na posição: {drone.cur_loc}")
print(f"Tesouros restantes: {len(drone.treasures) - len(drone.visited_treasures)}")

# ----------------------------
# FINALIZAÇÃO DA MISSÃO
# ----------------------------
drone.land()

# Nota: O gráfico permanecerá aberto até você fechar manualmente
