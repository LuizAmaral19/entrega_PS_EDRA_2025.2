from tello_sim_EDRA import Simulator

meu_Tello = Simulator()

# --- parâmetros ---
fov_Tello  = meu_Tello.vision_range
fov_by_2   = fov_Tello / 2.0
overlap    = 5.0

# Coordenadas globais (com nomes corrigidos)
global_rsl = meu_Tello.field_limit   # right
global_usl = meu_Tello.field_limit   # up
global_lsl = -meu_Tello.field_limit  # left
global_dsl = -meu_Tello.field_limit  # down

# Exemplo de células (ajuste se necessário)
cell1_rsl = meu_Tello.field_limit - fov_Tello   # limite direito da célula 1
cell1_dsl = -fov_by_2                           # limite inferior da célula 1

# -------------------------
# Função que gera o zig-zag de cobertura para a célula 1
# -------------------------
def sweeping_cell1():
    movements = []

    # dimensão vertical da região a varrer (de cima até a base da célula)
    height = global_usl - cell1_dsl
    step = fov_Tello

    # quantos passos inteiros cabem e se há parte fracionária
    full_sweeps = int(height // step)        # número de passos inteiros (floor)
    remainder = height - full_sweeps * step  # sobra (pode ser 0)

    # helpers para calcular distância horizontal no momento da execução
    def horizontal_right():
        return max(0.0, abs(cell1_rsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)

    def horizontal_left():
        return max(0.0, abs(global_lsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)

    # Construir zig-zag: (back step) + (horizontal move) repetido
    # Note: se full_sweeps for 0, não adicionamos nada
    for i in range(full_sweeps):
        # passo vertical (descer)
        movements.append((meu_Tello.back, (lambda s=step: s)))
        # passo horizontal alternado
        if i % 2 == 0:
            movements.append((meu_Tello.right, horizontal_right))
        else:
            movements.append((meu_Tello.left, horizontal_left))

    # se existir resto, desce o resto e faz o movimento horizontal final
    if remainder > 1e-6:
        movements.append((meu_Tello.back, (lambda r=remainder: r)))
        # direção do movimento final depende da paridade dos passos já feitos
        if full_sweeps % 2 == 0:
            movements.append((meu_Tello.right, horizontal_right))
        else:
            movements.append((meu_Tello.left, horizontal_left))

    return movements

# -------------------------
# Movimentos iniciais (posição de entrada na célula)
# -------------------------
movements_cell1 = [
    (meu_Tello.right, lambda: max(0.0, abs(global_rsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
    (meu_Tello.forward, lambda: max(0.0, abs(global_usl - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)),
    (meu_Tello.left, lambda: max(0.0, abs(global_lsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
]

# anexar corretamente a lista retornada por sweeping_cell1 (não append!)
movements_cell1.extend(sweeping_cell1())

# -------------------------
# Função que executa movimentos em passos do tamanho do FOV
# e checa a cada passo se todos os tesouros foram coletados.
# Retorna True se terminou (pegou todos); False caso contrário.
# -------------------------
def move_and_check(drone, command, distance_or_fn):
    # obtém distância numérica (se for callable, chama)
    distance = distance_or_fn() if callable(distance_or_fn) else distance_or_fn

    # protege contra distâncias negativas/zero
    if distance is None or distance <= 1e-6:
        return False

    step = fov_Tello
    full_steps = int(distance // step)
    remainder = distance - full_steps * step

    # passos inteiros
    for _ in range(full_steps):
        command(step)
        # checar se terminou
        if len(drone.visited_treasures) >= len(drone.treasures):
            return True

    # passo final (resto)
    if remainder > 1e-6:
        command(remainder)
        if len(drone.visited_treasures) >= len(drone.treasures):
            return True

    return False

# -------------------------
# go_home simplificado
# -------------------------
def go_home():
    x, y = meu_Tello.cur_loc
    # mover em y
    if y > 0:
        meu_Tello.back(y)
    elif y < 0:
        meu_Tello.forward(-y)
    # mover em x
    if x > 0:
        meu_Tello.left(x)
    elif x < 0:
        meu_Tello.right(-x)
    meu_Tello.land()

# -------------------------
# rotina principal
# -------------------------
def area_coverage():
    meu_Tello.takeoff()
    for command, dist_fn in movements_cell1:
        finished = move_and_check(meu_Tello, command, dist_fn)
        if finished:
            break

# executar
area_coverage()
go_home()
