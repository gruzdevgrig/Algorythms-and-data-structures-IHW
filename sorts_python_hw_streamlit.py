import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from scipy.optimize import curve_fit

# ==========================================
# 1. РЕАЛИЗАЦИЯ АЛГОРИТМОВ (СОГЛАСНО ТЗ)
# ==========================================

def counting_sort(arr: list) -> tuple[list, int]:
    '''Сортировка подсчетом.
        Возвращает: (отсортированный_массив, comparisons, swaps)
        Сложность: O(N + k) по времени, O(k) по памяти.'''
    swaps = 0 #счетчик перезаписей и перестановок
    comparisons = 0
    max_val = max(arr) 
    min_val = min(arr) 
    count_list = [0] * (max_val - min_val +1) #делаем массив нулей длиной с рабочий диапазон, чтобы расположить количества данного значения на месте его расположения в рабочем диапазоне
    for num in arr:
        count_list[num - min_val] += 1
        swaps += 1 #записываем каждый подсчет количества в счетчик перезаписей и перестановок
    arr.clear()
    for i in range(min_val, max_val + 1):
        index = i - min_val #индекс в массиве подсчетов, по которому ищем значение 
        for _ in range(count_list[index]):
            arr.append(i)
            swaps += 1 #записываем каждое добавление в результирующий массив в счетчик перезаписей и перестановок
    return arr, swaps, comparisons

def ins_sort(arr: list) -> tuple[list, int, int]:
    '''Сортировка вставкой.
        Возвращает: (отсортированный_массив, comparisons, swaps)
        Сложность: O(N^2) по времени, O(1) по памяти.'''
    comparisons = 0 #счетчик сравнений
    swaps = 0 #счетчик перестановок и перезаписей
    for i in range(1, len(arr)):
        base_el = arr[i] #на время одной итерации присваиваем i-тому элементу статус базового
        j = i - 1 
        while j >= 0:
            comparisons += 1 #за каждое сравнение с i-тым элементом
            if arr[j] > base_el:
                arr[j+1] = arr[j] #перетаскивание меньшего элемента влево
                swaps += 1 #за перетаскивание
                j -= 1 #смещение элемента с которым сравниваем
            else: break
        arr[j+1] = base_el #перезаписываем базовый элемент на новое место, если надо(если не надо, он останется там же и тут же сменится на новой итерации цикла)
        swaps += 1 #за перезапись базового элемента
    return arr, swaps, comparisons



def bubble_sort(arr: list[int | float]) -> tuple[list[int | float], int, int]:
    """
    Сортировка пузырьком с флаговой оптимизацией.
    Возвращает: (отсортированный_массив, comparisons, swaps)
    
    Временная сложность: O(N^2) в худшем и среднем случае, O(N) в лучшем.
    Пространственная сложность: O(1).
    """
    comparisons = 0 #да уже понятно че это
    swaps = 0 #да уже понятно че это
    n = len(arr)
    for i in range(n - 1): 
        swapped = False #флаг: были ли перестановки на текущем проходе
        for j in range(n - i - 1): 
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j] #перетаскиваие большего элемента вправо
                swaps += 1 #за перетаскивание
                swapped = True #фиксируем, что произошла перестановка
        if not swapped: #если за весь проход не было ни одной перестановки, значит массив уже отсортирован, и можно досрочно завершить работу
            break      
    return arr, comparisons, swaps
# ==========================================
# 2. ГЕНЕРАЦИЯ ДАННЫХ (СОГЛАСНО ТЗ)
# ==========================================

def generate_data(n: int, dist_type: str, seed: int = 42) -> list:
    """Генерирует массивы 5 типов распределений."""
    np.random.seed(seed) #генерация сида, чтобы в каждую сортировку для чистоты эксперимента поступал один и тот же массив
    
    if dist_type == "Random":
        return np.random.randint(0, n, size=n).tolist() #tolist - переводит массив нумпая в стандартный массив питона
    
    elif dist_type == "Sorted":
        return list(range(n))
    
    elif dist_type == "Reversed":
        return list(range(n, 0, -1))
    
    elif dist_type == "Nearly Sorted":
        arr = list(range(n))
        # Меняем местами 5% элементов
        for _ in range(int(n * 0.05)):
            i = np.random.randint(0, n)
            j = np.random.randint(0, n)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    
    elif dist_type == "Many Duplicates":
        return np.random.choice([1, 2, 3, 4, 5], size=n).tolist()
    
    return []


# ==========================================
# 3. ИНТЕРФЕЙС STREAMLIT
# ==========================================

st.set_page_config(page_title="Бенчмаркинг сортировок", layout="wide")
st.title("📊 ИДЗ: Эмпирический анализ алгоритмов сортировки")

# --- Сайдбар (Панель управления) ---
st.sidebar.header("Настройки эксперимента")

# Выбор алгоритмов
algorithms = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": ins_sort,
    "Counting Sort": counting_sort
}
selected_algos = st.sidebar.multiselect(
    "Выберите алгоритмы:", 
    list(algorithms.keys()), 
    default=["Bubble Sort", "Counting Sort", "Insertion Sort"]
)

# Выбор типа распределения
dist_type = st.sidebar.selectbox(
    "Тип входных данных:",
    ["Random", "Sorted", "Reversed", "Nearly Sorted", "Many Duplicates"]
)

# Выбор размера массива (сетка из ТЗ)
st.sidebar.subheader("Размер массива (N)")
N_options = st.sidebar.multiselect(
    "Выберите размеры N:",
    [100, 500, 1000, 2000, 5000, 10000, 20000],
    default=[100, 500, 1000, 2000]
)

# Число повторений (ТЗ требует 5-10)
repeats = st.sidebar.slider("Количество повторов (для усреднения):", 1, 10, 5)

# Кнопка запуска
run_btn = st.sidebar.button("🚀 Запустить бенчмаркинг")

# --- Основная логика ---
if run_btn:
    if not selected_algos or not N_options:
        st.error("Выберите хотя бы один алгоритм и один размер массива.")
    else:
        st.info(f"Запуск тестов. Тип данных: **{dist_type}**. Повторов: **{repeats}**.")
        
        results = []
        progress_bar = st.progress(0)
        total_steps = len(selected_algos) * len(N_options)
        step = 0
        
        for algo_name in selected_algos:
            func = algorithms[algo_name]
            
            for n in N_options:
                times = []
                comparisons = 0
                swaps = 0
                
                for _ in range(repeats):
                    # Генерация и копирование ВНЕ замера
                    data = generate_data(n, dist_type, seed=np.random.randint(0, 10000))
                    data_copy = data.copy()
                    
                    # Замер времени
                    t_start = time.perf_counter()
                    _, comparisons, swaps = func(data_copy)
                    t_end = time.perf_counter()
                    
                    times.append((t_end - t_start) * 1000) # в миллисекунды
                
                # Усреднение
                mean_time = np.mean(times)
                std_time = np.std(times)
                
                results.append({
                    "Алгоритм": algo_name,
                    "N": n,
                    "Среднее время (мс)": mean_time,
                    "Отклонение (мс)": std_time,
                    "Сравнения": comparisons,
                    "Перестановки": swaps
                })
                
                step += 1
                progress_bar.progress(step / total_steps)
                
        df = pd.DataFrame(results)
        
        # --- Вывод таблицы ---
        st.subheader("Сырые данные замеров")
        st.dataframe(df, use_container_width=True)
        
        # --- Графики ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("График 1: Время T(N) (Линейный масштаб)")
            fig_linear = go.Figure()
            for algo in selected_algos:
                algo_df = df[df["Алгоритм"] == algo]
                fig_linear.add_trace(go.Scatter(
                    x=algo_df["N"], 
                    y=algo_df["Среднее время (мс)"],
                    error_y=dict(type='data', array=algo_df["Отклонение (мс)"], visible=True),
                    mode='lines+markers',
                    name=algo
                ))
            fig_linear.update_layout(xaxis_title="Размер массива, N (элементов)",
                                     yaxis_title="Время выполнения, T (мс)",
                                     xaxis_type="linear", yaxis_type="linear")
            st.plotly_chart(fig_linear, use_container_width=True)
            
        with col2:
            st.subheader("График 2: Log-Log масштаб")
            fig_log = go.Figure()
            for algo in selected_algos:
                algo_df = df[df["Алгоритм"] == algo]
                # Исключаем нулевые значения для логарифма
                valid_df = algo_df[algo_df["Среднее время (мс)"] > 0]
                fig_log.add_trace(go.Scatter(
                    x=valid_df["N"], 
                    y=valid_df["Среднее время (мс)"],
                    mode='lines+markers',
                    name=algo
                ))
            fig_log.update_layout(xaxis_title="Размер массива, N (Log)",
                                  yaxis_title="Время выполнения, T (Log)",
                                  xaxis_type="log", yaxis_type="log")
            st.plotly_chart(fig_log, use_container_width=True)
            
        # --- Теоретическая аппроксимация (Fitting) ---
        st.subheader("График 3: Теоретическая аппроксимация (Fitting)")
        st.write("Здесь мы подбираем коэффициенты для теоретических сложностей O(N), O(N²), O(N log N).")
        
        fig_fit = go.Figure()
        
        # Определяем теоретические функции
        def f_linear(x, c): return c * x
        def f_nlogn(x, c): return c * x * np.log2(x)
        def f_quad(x, c): return c * x**2

        for algo in selected_algos:
            algo_df = df[df["Алгоритм"] == algo]
            x_data = algo_df["N"].values
            y_data = algo_df["Среднее время (мс)"].values
            
            # Сами точки
            fig_fit.add_trace(go.Scatter(x=x_data, y=y_data, mode='markers', name=f"{algo} (Данные)"))
            
            # Подбор кривой (в зависимости от алгоритма)
            try:
                if "Bubble" in algo or "Insertion" in algo:
                    popt, _ = curve_fit(f_quad, x_data, y_data, p0=[1e-6])
                    fig_fit.add_trace(go.Scatter(x=x_data, y=f_quad(x_data, *popt), mode='lines', name=f"{algo} (Теория O(N²))", line=dict(dash='dash')))
                elif "Counting" in algo:
                    popt, _ = curve_fit(f_linear, x_data, y_data, p0=[1e-6])
                    fig_fit.add_trace(go.Scatter(x=x_data, y=f_linear(x_data, *popt), mode='lines', name=f"{algo} (Теория O(N))", line=dict(dash='dash')))
            except:
                st.warning(f"Не удалось построить аппроксимацию для {algo} (недостаточно точек или неверный масштаб).")
                
        fig_fit.update_layout(xaxis_title="Размер массива, N",
                              yaxis_title="Время выполнения, T (мс)",
                              xaxis_type="linear", yaxis_type="linear")
        st.plotly_chart(fig_fit, use_container_width=True)