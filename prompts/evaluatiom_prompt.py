EVALUATION_PROMPT = """
You are an AI engineer.

Generate Python code to evaluate a TensorFlow image classification model.

STRICT REQUIREMENTS:
- Do NOT skip any step
- Code must match production-level evaluation
- Output ONLY executable Python code
- NEVER access class_names after dataset.map()
- ALWAYS store class_names before mapping
- DO NOT use 'state'
- Final output must be stored in a variable named 'evaluation_result'
- Prediction logic (STRICT):
    - If preds.shape[-1] == 1:
        pred_labels = (preds > 0.5).astype(int).flatten()

    - Else:
        pred_labels = np.argmax(preds, axis=1)

    - DO NOT use axis=0
    - DO NOT skip flatten()
    - DO NOT simplify this logic
- Use labels.numpy()
- Use extend(), not append()

REQUIREMENTS:

1. Load model:
tf.keras.models.load_model(
    "models/trained_model/casting_defect_model.keras",
    compile=False,
    safe_mode=False
)

2. Load dataset using:
dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    image_size=(224,224),
    batch_size=32,
    shuffle=False
)

3. IMPORTANT:
- Extract class_names BEFORE normalization:
class_names = dataset.class_names

4. Normalize dataset:
dataset = dataset.map(lambda x, y: (x / 255.0, y))

5. Prediction loop:
- Iterate batch-wise
- Collect all_preds and all_labels

6. Handle BOTH cases:
- Binary: (preds > 0.5)
- Multi-class: argmax

7. Compute metrics:
- You MUST calculate metrics using sklearn.metrics exactly as follows:

- from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

- accuracy = accuracy_score(all_labels, all_preds)
- precision = precision_score(all_labels, all_preds, average="binary")
- recall = recall_score(all_labels, all_preds, average="binary")
- f1 = f1_score(all_labels, all_preds, average="binary")
- cm = confusion_matrix(all_labels, all_preds)

- Do NOT approximate or reuse accuracy for other metrics.
- Do NOT manually calculate metrics.
- Do NOT simplify formulas.

8. Dataset statistics (VERY IMPORTANT):
- Extract class_names from dataset
- For EACH class folder:
    count = len(os.listdir(class_folder))
- Build:
    class_distribution = {{}}
    total_images = sum

9. Final output MUST be:

result = {{
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1": f1,
    "confusion_matrix": cm.tolist(),
    "total_images": total_images,
    "class_distribution": class_distribution
}}

10. Save result into:
evaluation_result = result

11. DO NOT skip dataset statistics
12. DO NOT assume values
13. DO NOT simplify logic

Dataset path:
{dataset_path}
"""