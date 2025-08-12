# 📚 algorithms-study

A collection of sorting algorithm implementations and benchmarks focused on performance and practical comparison.

---

## 🧪 Benchmark Results (500 Elements)

| Algorithm       | Execution Time (500 elements)       |
|-----------------|-------------------------------------|
| 🫧 **Bubble Sort**     | ⏱️ 21.69 seconds                    |
| 🪛 **Insertion Sort**  | ⏱️ 44.37 seconds *(slower than Bubble)* |
| 🏁 **Ranking Sort**    | ⚡ 0.23 seconds *(very fast)*         |
| 🏁 **Python Sort sorted()**    | ⚡ 0.003 seconds *(ultra fast)*         |

---

## 📝 Summary

- **Bubble Sort** performs better than Insertion Sort in this test but is still inefficient for large datasets.
- **Insertion Sort** can be faster than Bubble Sort on nearly sorted data but struggles with random data.
- **Ranking Sort** (likely based on counting or index mapping) dramatically outperforms both due to linear time complexity under the right constraints.

---

## 🚀 Goals

- Understand real-world performance differences.
- Analyze behavior of classic algorithms.
- Compare time complexities with actual execution times.

---

## 🔧 How to Run

1. Clone this repository.
2. Ensure Python 3 is installed.
3. Run each sort script:
   ```bash
   python bubble_sort.py
   python insertion_sort.py
   python ranking_sort.py
