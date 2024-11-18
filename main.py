import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


nfa_transitions: dict = {
    "A": {"a": "A1", "b": "C1", "c": "C"},
    "A1": {"b": "B"},
    "B": {"b": "B", "c": "B1"},
    "B1": {},
    "C": {"b": "C1", "c": "C"},
    "C1": {"c": "C2"},
    "C2": {},
    "S": {"a": ("A1", "S1"), "b": ("B", "C1"), "c": ("C", "B1")},
    "S1": {"a": "S"},
}
current_statenfa = "S"
alphabet: str = "abcABC"
nfa_nodes: list = [("S"), ("B1"), ("C1"), ("A1"), ("C2"), ("S1"), ("B"), ("C"), ("A")]
current_state = "B"

dfa_transitions: dict = {
    "A": {"a": "B", "b": "C"},
    "B": {"a": "A", "b": "D", "c": "E"},
    "C": {"b": "C", "c": "F"},
    "D": {"b": "C", "c": "G"},
    "E": {"b": "H", "c": "I"},
    "F": {},
    "G": {},
    "H": {"c": "J"},
    "I": {"b": "H", "c": "I"},
    "J": {},
}

dfa_nodes: list = [
    ("A", {"relevant_states": ["S1", "A1"]}),
    ("B", {"relevant_states": ["S"]}),
    ("C", {"relevant_states": ["B"]}),
    ("D", {"relevant_states": ["C1", "B"]}),
    ("E", {"relevant_states": ["C", "B1"]}),
    ("F", {"relevant_states": ["B1"]}),
    ("G", {"relevant_states": ["B1", "C2"]}),
    ("H", {"relevant_states": ["C1"]}),
    ("I", {"relevant_states": ["C"]}),
    ("J", {"relevant_states": ["C2"]}),
]

D = nx.DiGraph()
D.add_nodes_from(dfa_nodes)
for state, transitions in dfa_transitions.items():
    for symbol, next_states in transitions.items():
        if isinstance(next_states, tuple):
            for next_state in next_states:
                D.add_edge(state, next_state, label=symbol)
        else:
            D.add_edge(state, next_states, label=symbol)

# Приймаючі стани
accepting_statesnfa = ["C2", "B1"]
accepting_statesdfa = ["E", "F", "G", "J"]

G = nx.DiGraph()
G.add_nodes_from(nfa_nodes)

for state, transitions in nfa_transitions.items():
    for symbol, next_states in transitions.items():
        if isinstance(next_states, tuple):
            for next_state in next_states:
                G.add_edge(state, next_state, label=symbol)
        else:
            G.add_edge(state, next_states, label=symbol)

pos = {
    "A": (-2, 2),  # Вузол A у верхньому лівому куті
    "A1": (-2, 0),  # A1 розташований лівіше та нижче
    "B": (-1, 0.5),  # B розташований прямо над S
    "B1": (-1, -1),  # B1 ліворуч і нижче S
    "S": (0, 0),  # S у центрі
    "S1": (0, 1),  # S1 прямо під S
    "C": (2, 2),  # C праворуч і вгору від S
    "C1": (2, 0),  # C1 правіше від C
    "C2": (2, -1),  # C2 під C1
}



def build_graph(current_state, possible_states):
    color_map = []
    for node in G.nodes:
        if node in possible_states:
            color_map.append("yellow")
        elif node == current_statenfa:
            color_map.append("green")
        elif node in accepting_statesnfa:
            color_map.append("lightblue")
        else:
            color_map.append("lightgray")

    ax.clear()
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=color_map,
        node_size=1000,
        font_color="black",
        font_size=10,
        font_family="Times New Roman",
        edge_color="black",
        width=2,
        ax=ax,
    )

    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        label_pos=0.5,
        font_color="black",
        font_size=10,
        font_family="Times New Roman",
        ax=ax,
    )
    canvas.draw()


def on_key(event):
    global current_state
    key = event.char
    if key not in alphabet:
        print(f"Недопустимий символ: {key}")
        return

    if key == "q":
        print("Програма завершена.")
        
        
    relevant_states = nx.get_node_attributes(D, "relevant_states")
    next_state = dfa_transitions[current_state].get(key)
    print(next_state)
    if next_state:
        print(current_state)
        current_state = next_state
        print(relevant_states[current_state])
        possible_states = relevant_states[current_state]
        build_graph(current_state, possible_states)
    else:
        print("Перехід не визначено.")

    print(f"Поточний стан: {current_state}")
    if current_state in accepting_statesdfa:
        print("Частина рядка приймається автоматом.")

    if current_state in accepting_statesdfa:
        print("Рядок прийнятий автоматом.")
    else:
        print("Рядок не прийнятий автоматом.")


# Налаштування Tkinter
root = tk.Tk()
root.title("NFA Visualization")

fig, ax = plt.subplots(figsize=(6, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

build_graph(current_state, [])

# Обробка клавіш
root.bind("<Key>", on_key)

print("Натискайте клавіші ('a', 'b', 'c') для введення символів. Натисніть 'q' для виходу.")
def restart():
    global current_state
    current_state = "B"  # Сбрасываем в начальное состояние
    build_graph(current_state, [])  # Обновляем граф
    print("Автомат перезапущен. Текущее состояние: S")

# Кнопка Restart
restart_button = tk.Button(root, text="Restart", command=restart, font=("Times New Roman", 14))
restart_button.pack(pady=10)

def exit_program():
    print("Программа завершена.")
    root.quit()
    root.destroy()  # Закрытие окна tkinter

# Кнопка Exit
exit_button = tk.Button(root, text="Exit", command=exit_program, font=("Times New Roman", 14))
exit_button.pack(pady=10)

root.mainloop()
