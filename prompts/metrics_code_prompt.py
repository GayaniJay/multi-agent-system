METRICS_CODE_PROMPT = """
You are a senior AI engineer.

Your task is to generate Python code that EXACTLY reproduces the chart and table generation logic described below.

You MUST follow the instructions strictly. Any deviation is NOT allowed.

==============================
INPUT DATA
==============================
{evaluation_result}

==============================
REQUIRED VARIABLES
==============================
You MUST define:

accuracy
precision
recall
f1
class_distribution (dict)
cm (2D list)

==============================
METRICS TABLE FORMAT (STRICT)
==============================
metrics_table_data = [
    ["指標", "値"],
    ["正解率 (Accuracy)", round(accuracy, 4)],
    ["適合率 (Precision)", round(precision, 4)],
    ["再現率 (Recall)", round(recall, 4)],
    ["F1スコア (F1 Score)", round(f1, 4)]
]

==============================
CHART 1: METRICS BAR CHART (STRICT)
==============================
plt.figure()
plt.bar(["Accuracy", "Precision", "Recall", "F1"], [accuracy, precision, recall, f1])
plt.title("Evaluation Metrics")
plt.ylabel("Score")
plt.ylim(0, 1)
plt.grid(axis="y")
plt.savefig("outputs/reports/metrics.png")
plt.close()

==============================
CHART 2: CONFUSION MATRIX (STRICT)
==============================
class_names = list(class_distribution.keys())
cm_array = np.array(cm)

plt.figure()
plt.imshow(cm_array, cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.colorbar()
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.xticks(range(len(class_names)), class_names)
plt.yticks(range(len(class_names)), class_names)

thresh = cm_array.max() / 2.0

for i in range(len(cm_array)):
    for j in range(len(cm_array[0])):
        color = "white" if cm_array[i][j] > thresh else "black"
        plt.text(j, i, cm_array[i][j], ha="center", va="center", color=color, fontweight='bold')

plt.savefig("outputs/reports/confusion_matrix.png")
plt.close()

==============================
OTHER REQUIREMENTS
==============================
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("outputs/reports", exist_ok=True)

==============================
OUTPUT RULES
==============================
- Output ONLY Python code
- No explanation
- No markdown
- No comments
"""