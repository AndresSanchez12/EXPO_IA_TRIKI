# triki_streamlit.py
import streamlit as st
from collections import deque
import time

class TrikiBFS:
    def __init__(self):
        # Inicializar estado en session_state
        if 'tablero' not in st.session_state:
            st.session_state.tablero = [' '] * 9
            st.session_state.turno = 'X'
            st.session_state.juego_activo = True
            st.session_state.mensaje = "¡Tu turno! (X)"
            st.session_state.combo_ganador = None
    
    def verificar_ganador(self, tablero, jugador):
        combinaciones = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for combo in combinaciones:
            if all(tablero[i] == jugador for i in combo):
                return True, combo
        return False, None
    
    def verificar_empate(self, tablero):
        return ' ' not in tablero
    
    def bfs_encontrar_victoria(self, tablero_inicial):
        # Ver si podemos ganar ahora
        for i in range(9):
            if tablero_inicial[i] == ' ':
                tablero_inicial[i] = 'O'
                if self.verificar_ganador(tablero_inicial, 'O')[0]:
                    tablero_inicial[i] = ' '
                    return i
                tablero_inicial[i] = ' '
        
        # BFS para encontrar camino a victoria
        visitados = set()
        cola = deque()
        cola.append((tuple(tablero_inicial), None, 0))
        visitados.add(tuple(tablero_inicial))
        
        while cola:
            estado, movimiento, profundidad = cola.popleft()
            tablero_actual = list(estado)
            
            if profundidad % 2 == 0:  # Turno de IA (O)
                for i in range(9):
                    if tablero_actual[i] == ' ':
                        tablero_actual[i] = 'O'
                        if self.verificar_ganador(tablero_actual, 'O')[0]:
                            if movimiento is not None:
                                return movimiento
                            return i
                        nuevo_estado = tuple(tablero_actual)
                        if nuevo_estado not in visitados:
                            visitados.add(nuevo_estado)
                            primero = movimiento if movimiento is not None else i
                            cola.append((nuevo_estado, primero, profundidad + 1))
                        tablero_actual[i] = ' '
            else:  # Turno del jugador (X)
                for i in range(9):
                    if tablero_actual[i] == ' ':
                        tablero_actual[i] = 'X'
                        nuevo_estado = tuple(tablero_actual)
                        if nuevo_estado not in visitados:
                            visitados.add(nuevo_estado)
                            cola.append((nuevo_estado, movimiento, profundidad + 1))
                        tablero_actual[i] = ' '
        
        # Heurística si no encuentra victoria
        if tablero_inicial[4] == ' ':
            return 4
        for i in [0, 2, 6, 8]:
            if tablero_inicial[i] == ' ':
                return i
        for i in range(9):
            if tablero_inicial[i] == ' ':
                return i
        return None
    
    def hacer_movimiento_ia(self):
        if not st.session_state.juego_activo or st.session_state.turno != 'O':
            return
        
        tablero = st.session_state.tablero.copy()
        mejor_pos = self.bfs_encontrar_victoria(tablero)
        
        if mejor_pos is not None:
            st.session_state.tablero[mejor_pos] = 'O'
            
            ganador, combo = self.verificar_ganador(st.session_state.tablero, 'O')
            if ganador:
                st.session_state.juego_activo = False
                st.session_state.mensaje = "¡Perdiste!"
                st.session_state.combo_ganador = combo
                return
            
            if self.verificar_empate(st.session_state.tablero):
                st.session_state.juego_activo = False
                st.session_state.mensaje = "¡Empate! "
                return
            
            st.session_state.turno = 'X'
            st.session_state.mensaje = "¡Tu turno! (X)"
    
    def hacer_movimiento_jugador(self, pos):
        if not st.session_state.juego_activo or st.session_state.turno != 'X':
            return
        if st.session_state.tablero[pos] != ' ':
            return
        
        st.session_state.tablero[pos] = 'X'
        
        ganador, combo = self.verificar_ganador(st.session_state.tablero, 'X')
        if ganador:
            st.session_state.juego_activo = False
            st.session_state.mensaje = "¡Ganaste! "
            st.session_state.combo_ganador = combo
            return
        
        if self.verificar_empate(st.session_state.tablero):
            st.session_state.juego_activo = False
            st.session_state.mensaje = "¡Empate! "
            return
        
        st.session_state.turno = 'O'
        st.session_state.mensaje = "Pensando... "
        st.rerun()
    
    def reiniciar(self):
        st.session_state.tablero = [' '] * 9
        st.session_state.turno = 'X'
        st.session_state.juego_activo = True
        st.session_state.mensaje = "¡Tu turno! (X)"
        st.session_state.combo_ganador = None

#  STREAMLIT 

def main():
    st.set_page_config(page_title="Triki", layout="centered")
    
    # Inicializar estado
    if 'tablero' not in st.session_state:
        st.session_state.tablero = [' '] * 9
        st.session_state.turno = 'X'
        st.session_state.juego_activo = True
        st.session_state.mensaje = "¡Tu turno! (X)"
        st.session_state.combo_ganador = None
    
    # Título
    st.title("Triki")
    st.markdown(f"### {st.session_state.mensaje}")
    
    # CSS para el tablero
    st.markdown("""
    <style>
    .casilla {
        width: 100px;
        height: 100px;
        font-size: 48px;
        font-weight: bold;
        border: 2px solid #333;
        background-color: #f0f0f0;
        cursor: pointer;
        transition: all 0.2s;
        text-align: center;
        line-height: 100px;
    }
    .casilla:hover {
        background-color: #e0e0e0;
        transform: scale(1.05);
    }
    .casilla-x {
        color: #2196F3;
    }
    .casilla-o {
        color: #f44336;
    }
    .casilla-ganador {
        background-color: #4CAF50 !important;
        color: white !important;
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    .tablero-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 4px;
        max-width: 320px;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Tablero
    st.markdown('<div class="tablero-container">', unsafe_allow_html=True)
    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            valor = st.session_state.tablero[i]
            
            if st.session_state.combo_ganador and i in st.session_state.combo_ganador:
                estilo = "casilla casilla-ganador"
            elif valor == 'X':
                estilo = "casilla casilla-x"
            elif valor == 'O':
                estilo = "casilla casilla-o"
            else:
                estilo = "casilla"
            
            juego = TrikiBFS()
            if st.button(
                valor if valor != ' ' else '',
                key=f"btn_{i}",
                use_container_width=True,
                disabled=(not st.session_state.juego_activo or 
                         st.session_state.turno != 'X' or 
                         valor != ' ')
            ):
                juego.hacer_movimiento_jugador(i)
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón de control (solo Nueva Partida)
    if st.button("Nueva Partida", use_container_width=True):
        juego = TrikiBFS()
        juego.reiniciar()
        st.rerun()
    
    # Turno de la IA
    if st.session_state.juego_activo and st.session_state.turno == 'O':
        juego = TrikiBFS()
        time.sleep(0.3)
        juego.hacer_movimiento_ia()
        st.rerun()

if __name__ == "__main__":
    main()